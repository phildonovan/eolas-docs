# Getting started

## 1. Get an API key

Sign up at [api.virtus-solutions.io](https://api.virtus-solutions.io/#signup). Your key will start with `vs_`.

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

=== "Python"

    ```python
    df = client.get("nz_cpi", start="2020-01-01")
    print(df.head())
    #          date  period   value
    # 0  2020-01-01  2020Q1  1010.0
    # 1  2020-04-01  2020Q2  1006.2
    ```

=== "R"

    ```r
    df <- vs_get("nz_cpi", start = "2020-01-01")
    head(df)
    #         date period  value
    # 1 2020-01-01 2020Q1 1010.0
    # 2 2020-04-01 2020Q2 1006.2
    ```

## 5. Browse available series

=== "Python"

    ```python
    series = client.list()
    # Returns a list of dicts with name, title, source, description
    ```

=== "R"

    ```r
    series <- vs_list()
    # Returns a data frame with name, title, source, description
    ```

You can also browse interactively at [api.virtus-solutions.io/series-browser](https://api.virtus-solutions.io/series-browser).

---

!!! tip "Rate limits"
    Free keys allow **1 request per day**. Upgrade to [Pro](https://api.virtus-solutions.io/#pricing) for unlimited requests.
