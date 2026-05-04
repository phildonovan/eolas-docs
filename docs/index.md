# vswarehouse

<div class="hero" markdown>

**Official Python and R clients for the vs-warehouse statistical data API.**

Access 187+ economic and demographic time series from Stats NZ, the ABS, and the OECD — in two lines of code, returning a data frame ready for analysis.

<div class="badge-row" markdown>

[![PyPI](https://img.shields.io/pypi/v/vswarehouse?label=PyPI&color=blue)](https://pypi.org/project/vswarehouse/)
[![R](https://img.shields.io/badge/R-GitHub-blue)](https://github.com/phildonovan/vswarehouse-r)
[![API](https://img.shields.io/badge/API-api.virtus--solutions.io-blue)](https://api.virtus-solutions.io)

</div>
</div>

---

## Choose your language

=== "Python"

    ```bash
    pip install vswarehouse
    ```

    ```python
    from vswarehouse import Client

    client = Client("vs_your_key")
    df = client.get("nz_cpi", start="2020-01-01")
    print(df.head())
    ```

=== "R"

    ```r
    remotes::install_github("phildonovan/vswarehouse-r")
    ```

    ```r
    library(vswarehouse)

    vs_key("vs_your_key")
    df <- vs_get("nz_cpi", start = "2020-01-01")
    plot(df$date, df$value, type = "l")
    ```

---

## What's in the API?

| Category | Examples |
|---|---|
| Macroeconomics | CPI, GDP growth, unemployment, interest rates |
| Labour & Earnings | Employment, wages, gender pay gap |
| Business & Enterprise | Firm counts, births/deaths, industry breakdowns |
| Population | Resident population by age, sex, ethnicity, region |
| Justice & Social | Charges, convictions, household expenditure |

Data is sourced from **Stats NZ**, the **Australian Bureau of Statistics**, and the **OECD**, updated weekly.

---

## Get an API key

Free tier (1 request/day) requires no credit card. [Get your key →](https://api.virtus-solutions.io/#signup)

For unlimited access, [upgrade to Pro](https://api.virtus-solutions.io/#pricing) ($49/month).
