# Getting started

## 1. Get an API key

Sign up at [api.virtus-solutions.io](https://api.virtus-solutions.io/signup). Your key will start with `vs_`.

## 2. Install the client

=== "Python"

    ```bash
    pip install vswarehouse
    ```

=== "R"

    ```r
    remotes::install_github("phildonovan/vswarehouse-r")
    ```

## 3. Set your key

=== "Python"

    Pass it directly:

    ```python
    from vswarehouse import Client
    client = Client("vs_your_key")
    ```

    Or set the environment variable and omit the argument:

    ```bash
    export VS_API_KEY=vs_your_key
    ```

    ```python
    client = Client()  # reads VS_API_KEY automatically
    ```

=== "R"

    Call `vs_key()` once per session:

    ```r
    library(vswarehouse)
    vs_key("vs_your_key")
    ```

    Or add it to your `.Renviron` for permanent access:

    ```
    VS_API_KEY=vs_your_key
    ```

## 4. Fetch your first series

Use source-specific helpers so your code is self-documenting:

=== "Python"

    ```python
    # Stats NZ
    df = client.statsnz("nz_cpi", start="2020-01-01")

    # OECD
    df = client.oecd("nz_gdp")

    # NZ Treasury
    df = client.treasury("treasury_fiscal_spending")

    print(df)
    # VSeries: nz_cpi [Stats NZ]
    # 20 rows
    #          date  period   value
    # 0  2020-01-01  2020Q1  1010.0
    # ...
    ```

=== "R"

    ```r
    # Stats NZ
    df <- vs_get_statsnz("nz_cpi", start = "2020-01-01")

    # OECD
    df <- vs_get_oecd("nz_gdp")

    # NZ Treasury
    df <- vs_get_treasury("treasury_fiscal_spending")

    df
    # vs_series: nz_cpi [Stats NZ]
    # 20 rows
    #         date period  value
    # 1 2020-01-01 2020Q1 1010.0
    # ...
    ```

## 5. Plot it

=== "Python"

    ```python
    df = client.statsnz("nz_cpi", start="2010-01-01")
    df.plot_series()   # matplotlib line chart, returns Axes
    ```

=== "R"

    ```r
    df <- vs_get_statsnz("nz_cpi", start = "2010-01-01")
    vs_plot(df)   # ggplot2 line chart, returns ggplot object
    ```

## 6. Browse available series

=== "Python"

    ```python
    client.list()              # all series
    client.list("Stats NZ")   # Stats NZ only
    ```

=== "R"

    ```r
    vs_list()            # all series
    vs_list_statsnz()    # Stats NZ only
    vs_list_oecd()       # OECD only
    vs_list_treasury()   # NZ Treasury only
    ```

You can also browse interactively at [api.virtus-solutions.io/series-browser](https://api.virtus-solutions.io/series-browser).

---

!!! tip "Rate limits"
    Free keys allow **3 requests per day**. Starter ($10/month) gives 10/day. [Pro](https://api.virtus-solutions.io/#pricing) ($49/month) is unlimited.
