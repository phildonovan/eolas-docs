# R client

The `eolas-data` R package provides a family of functions that wrap the eolas REST API and return **`eolas_dataset` data frames** ready for analysis with base R, dplyr, or ggplot2.

## Installation

```r
remotes::install_github("phildonovan/eolas-r")
```

Requires R 4.1+ and `httr2` 1.0+.

## Authentication

```r
library(eolas)

# Set for the session
eolas_key("your_eolas_key")
```

Or add to `.Renviron` for permanent, session-free access:

```
EOLAS_API_KEY=your_eolas_key
```

## Source-specific helpers

The recommended way to fetch data — the source is encoded in the function name, making code self-documenting and autocomplete-friendly in RStudio:

```r
df  <- eolas_get_statsnz("nz_cpi", start = "2020-01-01")   # Stats NZ
df  <- eolas_get_oecd("nz_gdp_growth")                      # OECD
df  <- eolas_get_rbnz("rbnz_b2_wholesale_rates_monthly")    # RBNZ
df  <- eolas_get_treasury("treasury_fiscal_spending")       # NZ Treasury
gdf <- eolas_get_linz("nz_parcels")   # LINZ (~3M rows — auto-bulks in seconds, no limit needed)
```

Source-specific helpers call `eolas_get()` internally and inherit smart routing: large and geospatial datasets auto-route through the cache+sync path, so `eolas_get_linz("nz_parcels")` returns an `sf` object in seconds — not 15 minutes. The first call emits a one-line message explaining what happened; subsequent calls are silent.

For cases where you want to be explicit, use `eolas_get_local()` (same path, extra options for `cache_dir` / `format` / `freshness`), or pass `mode = "live"` to hit the live Iceberg endpoint directly (useful for freshest data, OECD-restricted sources, or sliced queries with `limit`/`start`/`end`):

```r
# Explicit cache+sync path with extra control
gdf <- eolas_get_local("nz_parcels")
df  <- eolas_get_local("nz_cpi", cache_dir = "/data/eolas", format = "csv_gz")

# Force live scan — note: server returns 413 if the dataset is large/geo
# and no limit/start/end filter is set; apply a filter or use mode = "cached"
gdf <- eolas_get("nz_parcels", mode = "live")
```

See [Bulk downloads](../bulk-downloads.md) for the full routing rules and tier comparison.

Each returns a `eolas_dataset` tagged with the source label.

## Discovery

```r
eolas_list()                 # all datasets — tibble
eolas_list_statsnz()         # Stats NZ only
eolas_list_wellington()      # Wellington Region Councils only

eolas_search("HLFS")         # labour-force datasets (alias expansion)
eolas_search("OCR", source = "RBNZ")
eolas_search("kapiti")       # → kcdc_* council layers
eolas_search("cpi")          # ranks rbnz_m1_prices before nz_cpi; prints CPI guidance
```

`nz_cpi` is OECD year-on-year % change, not a CPI index level — use `rbnz_m1_prices` for quarterly index levels.

## eolas_dataset

All data-fetching functions return a `eolas_dataset` — a data frame with name and source metadata:

```r
df <- eolas_get_statsnz("nz_cpi", start = "2020-01-01")
df
# eolas_dataset: nz_cpi [Stats NZ]
# 20 rows
#         date period  value
# 1 2020-01-01 2020Q1 1010.0
# ...

attr(df, "eolas_name")    # "nz_cpi"
attr(df, "eolas_source")  # "Stats NZ"
```

`eolas_dataset` is fully compatible with dplyr, ggplot2, and any function that accepts a data frame.

## Plotting

`eolas_dataset` is a plain data frame — use ggplot2 (or base R) directly. `eolas_plot()` was removed in v1.3.0 because it silently mis-rendered datasets with multiple series per date. Plot the tidy data frame yourself instead:

```r
library(ggplot2)

df <- eolas_get_statsnz("nz_cpi", start = "2010-01-01")

ggplot(df, aes(date, value)) +
  geom_line() +
  ggplot2::labs(y = "Index (base 1000)")
```

Requires `ggplot2`: `install.packages("ggplot2")`.

## Working with large geo datasets

The 5.4M-row `linz.nz_parcels` table allocates ~10 GB when materialised as an `sf` object. Pass `as_arrow = TRUE` to skip all geometry materialisation and get a zero-copy `arrow::Table` instead — geometry stays as character WKT until you need it:

```r
# Zero-copy Arrow table — no sf allocation
tbl <- eolas_get_linz("nz_parcels", as_arrow = TRUE)

# Filter before materialising — dramatically cheaper than loading the full sf object
library(duckdb)
con <- dbConnect(duckdb())
result <- dbGetQuery(con, "
  SELECT parcel_id, geometry_wkt
  FROM tbl
  WHERE ST_Within(ST_GeomFromText(geometry_wkt),
                  ST_GeomFromText('POLYGON((174.7 -41.3, 174.8 -41.3, 174.8 -41.4, 174.7 -41.4, 174.7 -41.3))'))
")
```

`as_arrow = TRUE` works on all datasets (geo or non-geo), all routing modes (`mode = "live"`, `"cached"`, `"auto"`), and all `eolas_get_*()` source helpers. It cannot be combined with `as_sf = TRUE`.

## `eolas_integration()` (Enterprise plan)

Generate ready-to-run connector configs for popular data-pipeline tools:

```r
# Inspect the generated files without writing anything
result <- eolas_integration("meltano", c("nz_cpi", "nz_gdp_growth"))
names(result$files)            # "meltano.yml", "README.md", ".env.example"
cat(result$files$meltano.yml)

# Or write straight to a directory ready for `meltano install`
eolas_integration(
  "meltano",
  c("nz_cpi", "nz_gdp_growth"),
  output_dir = "./my-pipeline"
)
```

Platforms: `"meltano"`, `"fivetran"`, `"azure-data-factory"`.

This is an Enterprise-plan feature. Non-Enterprise keys see the server's upgrade message surfaced verbatim, with the pricing URL. The gating lives server-side so it's bypass-proof. See <https://eolas.fyi/#pricing>.

## Error handling

```r
tryCatch(
  eolas_get_statsnz("nz_cpi"),
  error = function(e) message("Error: ", conditionMessage(e))
)
```

| Condition | When raised |
|---|---|
| `"Authentication error: ..."` | Invalid or inactive key |
| `"Rate limit reached. ..."` | Daily limit reached |
| `"Not found: ..."` | Series identifier not found |
| `"API error (HTTP ...): ..."` | Unexpected API error |

## Attribution and provenance

Every `/data` response carries `X-Eolas-*` headers. The client merges them into
`eolas_meta()` automatically (v1.3.3+).

```r
df <- eolas_get("rbnz_b1_exchange_rates_monthly", limit = 5)
eolas_meta(df)$attribution_text
eolas_meta(df)$licence
```

For provenance in the JSON body, pass `envelope = TRUE`:

```r
df <- eolas_get("nz_cpi", limit = 5, envelope = TRUE)
eolas_meta(df)$data_sources
```

See [Getting started §5](../quickstart.md#5-attribution-and-provenance).

## Source

[github.com/phildonovan/eolas-r](https://github.com/phildonovan/eolas-r)
