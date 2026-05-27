# Reading our own GeoParquet was harder than it should have been

*2026-05-27 — Phil Donovan*

---

Last night a user asked whether `eolas_get_linz("nz_parcels")` was broken. It wasn't broken — but the warning it printed was confusing enough that a reasonable person would think so, and it was running almost two minutes on a table that should load in under thirty seconds. We investigated, found the root cause, and shipped a fix. Here's the honest account of how long that took and what we learned.

---

## The symptom

```r
gdf <- eolas_get_linz("nz_parcels")
```

```
eolas: auto-routing 'nz_parcels' through cache+sync (large/geo dataset).
       Cache lives at ~/.cache/eolas/. Use mode='live' to override.
Warning: GeoParquet read failed; fell back to WKT path. ...
Warning: eolas: 1147282 of 5431319 row(s) had no usable geometry ...
```

The data is correct. You get an `sf` object with 5.4 million rows. But the warnings look alarming, and the load time is around 95 seconds on warm cache — slow enough that a first-time user will assume something is fundamentally wrong with the file.

In Python the same dataset loads cleanly via `geopandas.read_parquet()` with no warnings. So the question became: what specifically is R's path doing differently?

---

## Wrong hypothesis #1: empty `geometry_types` metadata

Our GeoParquet files carry a file-level `geo` metadata block in the Parquet footer, which is what the [GeoParquet 1.1 spec](https://geoparquet.org/releases/v1.1.0/) requires. On inspection, the `geometry_types` array inside that block was empty — which is technically spec-noncompliant. We fixed this server-side the previous day (commit `7c46b94`) so that the metadata correctly declares `["MultiPolygon"]`.

This is a real fix that matters for spec compliance. But it didn't change the R behavior at all. `sfarrow::st_read_parquet()` still failed on `nz_parcels` after the metadata was correct.

## Wrong hypothesis #2: MultiPolygon-specific sfarrow bug

`doc_huts` (all Point geometries, ~3,500 rows) loaded fine through sfarrow. `nz_parcels` (MultiPolygons, 5.4M rows) didn't. The obvious inference: sfarrow has a bug with MultiPolygon geometries.

This turned out to be wrong in the wrong direction. The geometry type was a red herring. `doc_huts` has zero NULL-geometry rows. `nz_parcels` has 1.1 million of them — 21% of the table. That's the actual gating factor, not the geometry type.

## Wrong hypothesis #3: sfarrow is just broken on our files; switch to geoarrow R

`sfarrow` is effectively unmaintained (last commit 2023). The modern R ecosystem has moved toward the `geoarrow` package. The pitch is compelling — if your Parquet file carries GeoArrow extension metadata, reading it in R looks like:

```r
df <- arrow::read_parquet("file.parquet")
df$geom  # <geoarrow_vctr geoarrow.multipolygon{list}[100]>
```

No manual conversion. Native typed geometry. We tested this directly:

```r
library(geoarrow)
tbl <- arrow::read_parquet("nz_parcels.geo.parquet")
geoarrow::as_geoarrow_vctr(tbl$geometry)   # failed
geoarrow::as_geoarrow_array(tbl$geometry)  # failed
geoarrow::geoarrow_wkb(as.list(tbl$geometry))  # failed
```

All failed. The reason is explained in the next section, but the short version: `geoarrow` R is a low-level primitive toolkit for working with geometry objects that are *already* tagged with GeoArrow extension metadata. It is not a `read_geoparquet()` function. It provides typed-geometry constructors, schema parsing utilities, and writer helpers — but it won't auto-detect and decode a plain WKB binary column that happens to live in a GeoParquet file.

## The actual root cause

The real problem is a single validation in `sf::st_as_sfc.WKB`:

```r
stopifnot(inherits(x, "WKB"), vapply(x, is.raw, TRUE))
# Then internally: "cannot read WKB object from zero-length raw vector"
```

NULL geometries in our Parquet files are stored as zero-length raw vectors. When `sfarrow` hands those to `sf::st_as_sfc.WKB`, it aborts on the first one it encounters. One NULL in 5.4 million rows is enough to kill the entire read. `doc_huts` has no NULLs, so it worked. `nz_parcels` has 1.1 million, so it died immediately.

The fallback path — converting geometry to WKT strings and parsing those — handles NULLs correctly because an empty string is a valid R character value. That's why the data was technically correct despite the warning. But WKT serialization of 5.4 million polygon geometries is slow, which explains the 95-second load time.

---

## The fix

The fix is a new primary reader function, `.eolas_arrow_wkb_to_sf()`, in `eolas-r/R/bulk.R` (commit `24faab5`). The strategy is straightforward once you know the problem: split the rows into those with geometry and those without, decode the non-empty ones with `sf::st_as_sfc.WKB`, substitute `sf::st_geometrycollection()` for the empty ones, then recombine in order.

```r
.eolas_arrow_wkb_to_sf <- function(file_path) {
  tbl <- arrow::read_parquet(file_path)
  if (!"geometry" %in% names(tbl)) {
    stop(".eolas_arrow_wkb_to_sf: no 'geometry' column in ", file_path, call. = FALSE)
  }

  raw_list <- lapply(tbl$geometry, as.raw)
  non_empty <- vapply(raw_list, length, integer(1)) > 0L

  geom_list <- vector("list", length(raw_list))
  if (any(!non_empty)) {
    geom_list[!non_empty] <- list(sf::st_geometrycollection())
  }
  if (any(non_empty)) {
    decoded <- sf::st_as_sfc(
      structure(raw_list[non_empty], class = "WKB"),
      crs = 4326
    )
    geom_list[non_empty] <- decoded
  }
  sfc <- sf::st_sfc(geom_list, crs = 4326)

  attrs <- as.data.frame(tbl[, setdiff(names(tbl), "geometry"), drop = FALSE])
  sf::st_sf(attrs, geometry = sfc)
}
```

The reader hierarchy is now: arrow+WKB (primary) → sfarrow (safety net, still works on all-non-null Point datasets) → WKT-string (last resort). Two regression tests were added in `tests/testthat/test-bulk.R`: one checking that the function handles empty WKB rows without aborting, and one checking that it errors with a clear message when the geometry column is absent.

**Performance on `nz_parcels` (1.6 GB, 5.4M rows, Phil's laptop, warm cache):**

| Path | Time |
|---|---|
| New arrow+WKB path | 2.7 s |
| Previous WKT fallback | ~95 s |
| Speedup | ~35× |

Cold-cache real-world speedup is lower (network-bound), but still roughly 10× based on local SSD vs warm-cache ratio. Memory footprint is also lower: no intermediate character column for `geometry_wkt` gets allocated.

---

## Why `geoarrow_vctr` doesn't just work on our files

This is the part worth understanding if you're consuming GeoParquet from Apache Iceberg, DuckDB exports, or other non-GDAL writers.

There are two distinct encodings that produce `.parquet` files containing geometry:

| Encoding | Geometry column Arrow type | What `arrow::read_parquet()` returns in R |
|---|---|---|
| **GeoParquet** | plain `binary` + file-level `geo` metadata block | `arrow_binary` — needs manual decode |
| **GeoArrow-extension parquet** | `binary` + per-field Arrow extension metadata (`ARROW:extension:name=geoarrow.multipolygon` etc.) | `geoarrow_vctr` — native, no decode needed |

Our Parquet files come from pyiceberg. pyiceberg's current geometry support (merged in PR #2859, Feb 2026) maps geometry columns to `pa.large_binary()` — plain binary with no extension metadata attached per-field. The file-level `geo` block is present, which satisfies the GeoParquet spec and makes `geopandas.read_parquet()` happy in Python. But Arrow's R bindings have nothing to recognize at the column level, so it reads the column as a plain `arrow_binary` vector.

The `geoarrow` R package is built for the *second* encoding. It works beautifully when every geometry field carries `ARROW:extension:name` metadata — which is what you'd get from a GeoArrow-native writer. It doesn't know what to do with a file-level metadata block, and it makes no attempt to auto-detect the GeoParquet spec format.

This isn't a criticism of either package. They're solving different problems. The gap is at the writer layer: pyiceberg doesn't yet emit GeoArrow extension metadata per-field, so the seamless `geoarrow_vctr` experience isn't available for Iceberg-backed files yet.

---

## The Iceberg v3 path

The long-term solution is Iceberg v3 native geometry and geography types. The spec is published. pyiceberg has the type definitions. But the full chain from "spec exists" to "R reads it natively" is longer than it looks:

| Layer | Status | Realistic ETA |
|---|---|---|
| Iceberg v3 spec (geometry/geography types) | Done | Done |
| pyiceberg `GeometryType` / `GeographyType` (PR #2859) | Merged Feb 2026 — types defined, PyArrow mapping is plain `large_binary()` | pyiceberg 0.11.1 or 0.12 |
| pyiceberg full read/write with GeoArrow extension metadata | RFC #3004 open as of Feb 2026 | pyiceberg 0.12-0.13, **2026 Q3-Q4** |
| target-iceberg (the Singer target we use) consuming v3 types | Not started | After pyiceberg ships |
| Our taps emitting geometry-typed columns | Requires target-iceberg update | **2026 Q4 - 2027 Q1** |
| R/Python clients reading native `geoarrow_vctr` | Requires everything above + downstream Arrow + geoarrow R | **2027 Q1+** |

Minimum realistic window for eolas to be on the native path: 9-12 months. The shipped fix is not a stopgap we'll regret — it's the right thing for the horizon we're actually working in.

The upstream contribution that would compress this timeline is adding writer-side GeoArrow extension metadata emission to pyiceberg. The shape of that contribution, from the RFC:

```python
# Today: geometry_col → pa.large_binary()
# What unlocks native R reads:
pa.field("geom", pa.large_binary(), metadata={
    b"ARROW:extension:name": b"geoarrow.wkb",
    b"ARROW:extension:metadata": json.dumps({"crs": crs_string}).encode(),
})
```

The scope is roughly 200-400 lines of writer code plus tests, then 4-8 weeks of Apache review cycle. We've noted RFC #3004 to revisit post-launch. If the RFC has converged by then, a prototype PR is feasible.

---

## What's shipped

- `eolas-r` commit `24faab5` — `.eolas_arrow_wkb_to_sf()` primary reader, two regression tests, no behaviour change for datasets without NULL geometries
- The WKT-string fallback is preserved as a last resort; this is a non-breaking change
- `eolas_get_linz("nz_parcels")` now loads in under 3 seconds on warm cache with no warnings

The internal write-up lives in `eolas/docs/geoparquet-r-reader.md` (committed `bdefedd`), which has the full cross-reference map to the relevant pyiceberg PRs and specs.

---

*eolas is a New Zealand data API — eolas.fyi. The R client (`eolas`) and Python client (`eolas-data`) are available from GitHub and PyPI respectively.*
