# R API reference

## `vs_key(key)`

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

## `vs_list()`

Return metadata for all available series.

```r
series <- vs_list()
head(series[, c("name", "title", "source")])
#          name                    title source
# 1      nz_cpi  NZ Consumer Price Index   OECD
# 2 nz_gdp_grow         NZ GDP Growth      OECD
```

**Returns:** `data.frame` with columns `name`, `title`, `source`, `namespace`, `description`.

---

## `vs_info(name)`

Return metadata for a single series.

```r
meta <- vs_info("nz_cpi")
meta$title   # "NZ Consumer Price Index"
meta$source  # "OECD"
```

**Arguments**

| Name | Type | Description |
|---|---|---|
| `name` | character | Series identifier, e.g. `"nz_cpi"` |

**Returns:** Named `list`.

**Errors:** Stops with `"Not found: ..."` if the series does not exist.

---

## `vs_get(name, start = NULL, end = NULL)`

Fetch time-series data as a data frame.

```r
df <- vs_get("nz_cpi", start = "2020-01-01", end = "2024-12-31")
```

**Arguments**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | character | — | Series identifier |
| `start` | character \| NULL | `NULL` | ISO date lower bound, e.g. `"2020-01-01"` |
| `end` | character \| NULL | `NULL` | ISO date upper bound |

**Returns:** `data.frame` with columns:

| Column | Type | Description |
|---|---|---|
| `date` | `Date` | Observation date |
| `period` | character | Period label, e.g. `"2023Q1"` |
| `value` | numeric | Observed value |
| `dimensions` | character | Extra breakdown dimensions (empty string if none) |

**Errors:** Stops with a descriptive message for authentication, rate limit, and not-found errors.

---

## Common patterns

**With dplyr:**

```r
library(dplyr)
library(vswarehouse)

vs_key("vs_your_key")

vs_get("nz_cpi", start = "2015-01-01") |>
  filter(value > 1050) |>
  arrange(date)
```

**With ggplot2:**

```r
library(ggplot2)

df <- vs_get("nz_cpi", start = "2010-01-01")

ggplot(df, aes(date, value)) +
  geom_line(colour = "#3b82f6") +
  labs(title = "NZ Consumer Price Index", x = NULL, y = "Index") +
  theme_minimal()
```
