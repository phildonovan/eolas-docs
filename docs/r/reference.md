# R API reference

## Authentication

### `vs_key(key)`

Store an API key for the duration of the R session.

```r
vs_key("vs_your_key")
```

**Arguments**

| Name | Type | Description |
|---|---|---|
| `key` | character | A `vs_...` API key |

**Returns:** The key, invisibly.  
**Note:** If `VS_API_KEY` is set in the environment, you can skip this call entirely.

---

## Discovery

### `vs_list(source = NULL)`

Return metadata for all available series.

```r
vs_list()              # all series
vs_list("Stats NZ")   # Stats NZ only
```

**Arguments**

| Name | Type | Default | Description |
|---|---|---|---|
| `source` | character \| NULL | `NULL` | Filter by source label, e.g. `"Stats NZ"`, `"OECD"`. |

**Returns:** tibble (if `tibble` is installed) or `data.frame` with columns `name`, `title`, `source`, `namespace`, `description`.

---

### Source-specific list helpers

Convenience wrappers over `vs_list(source = ...)`.

| Function | Equivalent |
|---|---|
| `vs_list_statsnz()` | `vs_list("Stats NZ")` |
| `vs_list_oecd()` | `vs_list("OECD")` |
| `vs_list_rbnz()` | `vs_list("RBNZ")` |
| `vs_list_treasury()` | `vs_list("NZ Treasury")` |
| `vs_list_linz()` | `vs_list("LINZ")` |
| `vs_list_statsnz_geo()` | `vs_list("Stats NZ Geospatial")` |
| `vs_list_mbie()` | `vs_list("MBIE")` |
| `vs_list_nzta()` | `vs_list("Waka Kotahi")` |
| `vs_list_msd()` | `vs_list("MSD")` |
| `vs_list_police()` | `vs_list("NZ Police / MoJ")` |

---

### `vs_info(name)`

Return metadata for a single series.

```r
meta <- vs_info("nz_cpi")
meta$title   # "NZ Consumer Price Index"
meta$source  # "Stats NZ"
```

**Arguments**

| Name | Type | Description |
|---|---|---|
| `name` | character | Series identifier, e.g. `"nz_cpi"` |

**Returns:** Named `list`.  
**Errors:** Stops with `"Not found: ..."` if the series does not exist.

---

## Fetching data

### `vs_get(name, start = NULL, end = NULL, limit = NULL, as_sf = NULL)`

Generic workhorse. For everyday use prefer the source-specific helpers below.

```r
df  <- vs_get("nz_cpi", start = "2020-01-01", end = "2024-12-31")
df  <- vs_get("nz_addresses", limit = 1000)   # first 1000 rows
df  <- vs_get("nz_cpi")                       # full dataset (Pro tier)

# Geospatial: returns an sf object when the sf package is installed
gdf <- vs_get("nz_addresses", limit = 10)
plot(gdf["full_address"])                     # ready for mapping
sf::st_transform(gdf, 2193)                   # reproject to NZTM
```

**Arguments**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | character | — | Dataset identifier |
| `start` | character \| NULL | `NULL` | ISO date lower bound, e.g. `"2020-01-01"` |
| `end` | character \| NULL | `NULL` | ISO date upper bound |
| `limit` | integer \| NULL | `NULL` | Max rows. `NULL` requests the full dataset. Free / Starter plans are capped server-side at 50,000 rows; Pro is unlimited. |
| `as_sf` | logical \| NULL | `NULL` | Return an `sf` object for geospatial datasets. `NULL` auto-converts when geometry is present and the `sf` package is installed. `TRUE` forces conversion (errors if missing). `FALSE` keeps the raw `geometry_wkt` string column. Install with `install.packages("sf")`. |

**Returns:** `vs_series` data frame, or an `sf` object when geometry is present and conversion is enabled.

---

### Source-specific get helpers

Each is a named wrapper over `vs_get()` that tags the result with the source label.

| Function | Source |
|---|---|
| `vs_get_statsnz(name, start, end, limit, as_sf)` | Stats NZ |
| `vs_get_oecd(name, start, end, limit, as_sf)` | OECD |
| `vs_get_rbnz(name, start, end, limit, as_sf)` | RBNZ |
| `vs_get_treasury(name, start, end, limit, as_sf)` | NZ Treasury |
| `vs_get_linz(name, start, end, limit, as_sf)` | LINZ |
| `vs_get_statsnz_geo(name, start, end, limit, as_sf)` | Stats NZ Geospatial |
| `vs_get_mbie(name, start, end, limit, as_sf)` | MBIE |
| `vs_get_nzta(name, start, end, limit, as_sf)` | Waka Kotahi (NZTA) |
| `vs_get_msd(name, start, end, limit, as_sf)` | MSD |
| `vs_get_police(name, start, end, limit, as_sf)` | NZ Police / MoJ |

```r
df <- vs_get_statsnz("nz_cpi", start = "2015-01-01")
attr(df, "vs_source")   # "Stats NZ"
```

---

## Plotting

### `vs_plot(x)`

Quick ggplot2 line chart for a `vs_series`. Returns a `ggplot` object — add further layers with `+`.

```r
vs_get_statsnz("nz_cpi", start = "2010-01-01") |>
  vs_plot() +
  ggplot2::labs(y = "Index (base 1000)")
```

**Arguments**

| Name | Type | Description |
|---|---|---|
| `x` | vs_series | A data frame returned by any `vs_get_*()` function |

**Returns:** `ggplot` object.  
**Requires:** `ggplot2` — `install.packages("ggplot2")`.

---

## Common patterns

**With dplyr:**

```r
library(dplyr)
library(vswarehouse)

vs_key("vs_your_key")

vs_get_statsnz("nz_cpi", start = "2015-01-01") |>
  filter(value > 1050) |>
  arrange(date)
```

**With ggplot2 (manual):**

```r
library(ggplot2)

df <- vs_get_statsnz("nz_cpi", start = "2010-01-01")

ggplot(df, aes(date, value)) +
  geom_line(colour = "#3b82f6") +
  labs(title = "NZ Consumer Price Index", x = NULL, y = "Index") +
  theme_minimal()
```

**With vs_plot (quick):**

```r
df <- vs_get_statsnz("nz_cpi", start = "2010-01-01")
vs_plot(df)
```

**In R Markdown:**

````markdown
```{r setup, include=FALSE}
library(vswarehouse)
vs_key(Sys.getenv("VS_API_KEY"))
```

```{r cpi-chart, fig.cap="NZ Consumer Price Index"}
vs_get_statsnz("nz_cpi", start = "2015-01-01") |> vs_plot()
```
````
