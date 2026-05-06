# R client

The `vswarehouse` R package provides a family of functions that wrap the vs-warehouse REST API and return **`vs_series` data frames** ready for analysis with base R, dplyr, or ggplot2.

## Installation

```r
remotes::install_github("phildonovan/vswarehouse-r")
```

Requires R 4.1+ and `httr2` 1.0+.

## Authentication

```r
library(vswarehouse)

# Set for the session
vs_key("vs_your_key")
```

Or add to `.Renviron` for permanent, session-free access:

```
VS_API_KEY=vs_your_key
```

## Source-specific helpers

The recommended way to fetch data — the source is encoded in the function name, making code self-documenting and autocomplete-friendly in RStudio:

```r
df <- vs_get_statsnz("nz_cpi", start = "2020-01-01")   # Stats NZ
df <- vs_get_oecd("nz_gdp")                            # OECD
df <- vs_get_rbnz("ocr")                               # RBNZ
df <- vs_get_treasury("treasury_fiscal_spending")       # NZ Treasury
df <- vs_get_linz("nz_parcels")                        # LINZ
```

Each returns a `vs_series` tagged with the source label.

## Discovery

```r
vs_list()            # all series — tibble (or data.frame)
vs_list_statsnz()    # Stats NZ only
vs_list_oecd()       # OECD only
vs_list_rbnz()       # RBNZ only
vs_list_treasury()   # NZ Treasury only
vs_list_linz()       # LINZ only

# Generic filter
vs_list("Stats NZ")
```

## vs_series

All data-fetching functions return a `vs_series` — a data frame with name and source metadata:

```r
df <- vs_get_statsnz("nz_cpi", start = "2020-01-01")
df
# vs_series: nz_cpi [Stats NZ]
# 20 rows
#         date period  value
# 1 2020-01-01 2020Q1 1010.0
# ...

attr(df, "vs_name")    # "nz_cpi"
attr(df, "vs_source")  # "Stats NZ"
```

`vs_series` is fully compatible with dplyr, ggplot2, and any function that accepts a data frame.

## `vs_plot()`

One-line ggplot2 chart — returns a `ggplot` object you can customise further with `+`:

```r
vs_get_statsnz("nz_cpi", start = "2010-01-01") |>
  vs_plot() +
  ggplot2::labs(y = "Index (base 1000)")
```

Requires `ggplot2`: `install.packages("ggplot2")`.

## Error handling

```r
tryCatch(
  vs_get_statsnz("nz_cpi"),
  error = function(e) message("Error: ", conditionMessage(e))
)
```

| Condition | When raised |
|---|---|
| `"Authentication error: ..."` | Invalid or inactive key |
| `"Rate limit reached. ..."` | Daily limit reached |
| `"Not found: ..."` | Series identifier not found |
| `"API error (HTTP ...): ..."` | Unexpected API error |

## Source

[github.com/phildonovan/vswarehouse-r](https://github.com/phildonovan/vswarehouse-r)
