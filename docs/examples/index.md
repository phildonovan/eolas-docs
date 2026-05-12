# Examples

## Inflation over time (NZ CPI)

=== "Python"

    ```python
    from eolas_data import Client

    client = Client("vs_your_key")
    df = client.statsnz("nz_cpi", start="2010-01-01")
    df.plot_series()
    ```

=== "R"

    ```r
    library(eolas)

    eolas_key("vs_your_key")
    eolas_get_statsnz("nz_cpi", start = "2010-01-01") |> eolas_plot()
    ```

---

## Compare multiple series

=== "Python"

    ```python
    import pandas as pd
    import matplotlib.pyplot as plt

    client = Client("vs_your_key")

    cpi  = client.statsnz("nz_cpi",          start="2015-01-01")
    unem = client.oecd("nz_unemployment",     start="2015-01-01")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    cpi.plot_series(ax=ax1)
    unem.plot_series(ax=ax2)
    plt.tight_layout()
    plt.show()
    ```

=== "R"

    ```r
    library(ggplot2)
    library(patchwork)
    library(eolas)

    eolas_key("vs_your_key")

    p1 <- eolas_get_statsnz("nz_cpi",       start = "2015-01-01") |> eolas_plot()
    p2 <- eolas_get_oecd("nz_unemployment", start = "2015-01-01") |> eolas_plot()

    p1 / p2   # stacked with patchwork
    ```

---

## Discover and filter series

=== "Python"

    ```python
    # All Stats NZ series
    statsnz = client.list("Stats NZ")

    # All OECD series
    oecd = client.list("OECD")

    print(f"Stats NZ: {len(statsnz)} series, OECD: {len(oecd)} series")
    ```

=== "R"

    ```r
    # Source-specific list helpers
    statsnz <- eolas_list_statsnz()
    oecd    <- eolas_list_oecd()
    tsy     <- eolas_list_treasury()

    cat("Stats NZ:", nrow(statsnz), "series\n")
    cat("OECD:",     nrow(oecd),    "series\n")
    cat("Treasury:", nrow(tsy),     "series\n")
    ```

---

## Government fiscal data

=== "Python"

    ```python
    spending <- client.treasury("treasury_fiscal_spending", start="2000-01-01")
    debt     <- client.treasury("treasury_fiscal_debt",     start="2000-01-01")

    spending.plot_series()
    ```

=== "R"

    ```r
    spending <- eolas_get_treasury("treasury_fiscal_spending", start = "2000-01-01")
    debt     <- eolas_get_treasury("treasury_fiscal_debt",     start = "2000-01-01")

    eolas_plot(spending)
    ```

---

## Export to CSV

=== "Python"

    ```python
    df = client.statsnz("nz_cpi", start="2020-01-01")
    df.to_csv("nz_cpi.csv", index=False)
    ```

=== "R"

    ```r
    df <- eolas_get_statsnz("nz_cpi", start = "2020-01-01")
    write.csv(df, "nz_cpi.csv", row.names = FALSE)
    ```

---

## Notebook-friendly caching

=== "Python"

    ```python
    # cache=True means repeated runs don't re-hit the API
    client = Client(cache=True)

    df = client.statsnz("nz_cpi")   # fetched once
    df = client.statsnz("nz_cpi")   # from cache
    ```

=== "R"

    ```r
    # In R Markdown, wrap in a chunk with cache=TRUE
    ```

    ````markdown
    ```{r load-data, cache=TRUE}
    library(eolas)
    eolas_key(Sys.getenv("EOLAS_API_KEY"))
    df <- eolas_get_statsnz("nz_cpi", start = "2015-01-01")
    ```
    ````

---

## In R Markdown / Quarto

```r
---
title: "NZ Economic Overview"
---
```

````markdown
```{r setup, include=FALSE}
library(eolas)
library(ggplot2)
eolas_key(Sys.getenv("EOLAS_API_KEY"))
```

```{r cpi, fig.cap="NZ Consumer Price Index since 2010"}
eolas_get_statsnz("nz_cpi", start = "2010-01-01") |>
  eolas_plot() +
  labs(y = "Index (base 1000)")
```

```{r unemployment, fig.cap="NZ Unemployment Rate"}
eolas_get_oecd("nz_unemployment", start = "2010-01-01") |>
  eolas_plot() +
  labs(y = "Rate (%)")
```
````
