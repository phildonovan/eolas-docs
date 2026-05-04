# R client

The `vswarehouse` R package provides a set of functions that wrap the vs-warehouse REST API and return **data frames** ready for analysis with base R, `dplyr`, or `ggplot2`.

## Installation

```r
# Install from GitHub
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

Then just call `vs_list()`, `vs_info()`, or `vs_get()` — the key is found automatically.

## Functions at a glance

| Function | Returns | Description |
|---|---|---|
| `vs_key(key)` | key (invisibly) | Store API key for the session |
| `vs_list()` | `data.frame` | All series with metadata |
| `vs_info(name)` | `list` | Metadata for one series |
| `vs_get(name, ...)` | `data.frame` | Time-series data |

## Error handling

```r
tryCatch(
  vs_get("nz_cpi"),
  error = function(e) message("Error: ", conditionMessage(e))
)
```

Errors are plain R conditions with descriptive messages:

| Condition | When raised |
|---|---|
| `"Authentication error: ..."` | Invalid or inactive key |
| `"Rate limit reached. ..."` | Free-tier daily limit |
| `"Not found: ..."` | Series identifier not found |
| `"API error (HTTP ...): ..."` | Unexpected API error |

## Source

[github.com/phildonovan/vswarehouse-r](https://github.com/phildonovan/vswarehouse-r)
