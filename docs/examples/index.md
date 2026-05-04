# Examples

## Inflation over time (NZ CPI)

=== "Python"

    ```python
    import matplotlib.pyplot as plt
    from vswarehouse import Client

    client = Client("vs_your_key")
    df = client.get("nz_cpi", start="2010-01-01")

    plt.figure(figsize=(10, 4))
    plt.plot(df["date"], df["value"], color="#3b82f6")
    plt.title("NZ Consumer Price Index")
    plt.xlabel("")
    plt.ylabel("Index")
    plt.tight_layout()
    plt.show()
    ```

=== "R"

    ```r
    library(ggplot2)
    library(vswarehouse)

    vs_key("vs_your_key")
    df <- vs_get("nz_cpi", start = "2010-01-01")

    ggplot(df, aes(date, value)) +
      geom_line(colour = "#3b82f6") +
      labs(title = "NZ Consumer Price Index", x = NULL, y = "Index") +
      theme_minimal()
    ```

---

## Compare unemployment across time

=== "Python"

    ```python
    df = client.get("nz_unemployment", start="2000-01-01")

    # Mark recessions
    recessions = df[df["value"] > 6]
    print(f"Quarters above 6%: {len(recessions)}")
    ```

=== "R"

    ```r
    df <- vs_get("nz_unemployment", start = "2000-01-01")

    # Mark recessions
    high <- df[df$value > 6, ]
    cat("Quarters above 6%:", nrow(high), "\n")
    ```

---

## Discover available series

=== "Python"

    ```python
    import pandas as pd

    series = client.list()
    df = pd.DataFrame(series)

    # Find all OECD series
    oecd = df[df["source"] == "OECD"]
    print(oecd[["name", "title"]].to_string(index=False))
    ```

=== "R"

    ```r
    series <- vs_list()

    # Find all OECD series
    oecd <- series[series$source == "OECD", c("name", "title")]
    print(oecd, row.names = FALSE)
    ```

---

## Export to CSV

=== "Python"

    ```python
    df = client.get("nz_cpi", start="2020-01-01")
    df.to_csv("nz_cpi.csv", index=False)
    ```

=== "R"

    ```r
    df <- vs_get("nz_cpi", start = "2020-01-01")
    write.csv(df, "nz_cpi.csv", row.names = FALSE)
    ```

---

## Use in a Jupyter / R Markdown report

=== "Python"

    ```python
    # In a Jupyter notebook cell
    from vswarehouse import Client
    import os

    client = Client(os.environ["VS_API_KEY"])
    df = client.get("nz_gdp_growth")
    df.plot(x="date", y="value", title="NZ GDP Growth", legend=False)
    ```

=== "R"

    ````markdown
    ```{r setup, include=FALSE}
    library(vswarehouse)
    vs_key(Sys.getenv("VS_API_KEY"))
    ```

    ```{r cpi-chart}
    df <- vs_get("nz_cpi", start = "2015-01-01")
    plot(df$date, df$value, type = "l", main = "NZ CPI")
    ```
    ````
