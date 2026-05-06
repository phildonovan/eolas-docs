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

### `vs_get(name, start = NULL, end = NULL)`

Generic workhorse. For everyday use prefer the source-specific helpers below.

```r
df <- vs_get("nz_cpi", start = "2020-01-01", end = "2024-12-31")
```

**Arguments**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | character | — | Series identifier |
| `start` | character \| NULL | `NULL` | ISO date lower bound, e.g. `"2020-01-01"` |
| `end` | character \| NULL | `NULL` | ISO date upper bound |

**Returns:** `vs_series` data frame with `date` coerced to `Date`.

---

### Source-specific get helpers

Each is a named wrapper over `vs_get()` that tags the result with the source label.

| Function | Source |
|---|---|
| `vs_get_statsnz(name, start, end)` | Stats NZ |
| `vs_get_oecd(name, start, end)` | OECD |
| `vs_get_rbnz(name, start, end)` | RBNZ |
| `vs_get_treasury(name, start, end)` | NZ Treasury |
| `vs_get_linz(name, start, end)` | LINZ |

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
