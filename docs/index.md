# eolas-data

<div class="hero" markdown>

**Python, R, and command-line clients for the eolas API.**

1,500+ New Zealand economic, demographic and geospatial datasets, from Stats NZ, RBNZ, LINZ, Waka Kotahi (NZTA) and other agencies, as a data frame in two lines of code.

<div class="badge-row" markdown>

[![PyPI](https://img.shields.io/pypi/v/eolas-data?label=PyPI&color=blue)](https://pypi.org/project/eolas-data/)
[![R](https://img.shields.io/badge/R-GitHub-blue)](https://github.com/phildonovan/eolas-r)
[![API](https://img.shields.io/badge/API-api.eolas.nz-blue)](https://api.eolas.nz)

</div>
</div>

---

## What is eolas?

eolas is one API for official New Zealand data, with Python and R clients. The tables you would otherwise scrape or download from Stats NZ, RBNZ, LINZ and the rest come back through the same API.

Columns are typed. Dates are ISO, and column names are snake_case, on every source. Pipelines run on each agency's schedule (see the [status page](https://eolas.nz/status)). The REST API is on every plan. Bulk Parquet downloads are on Pro, Team, and Enterprise, not on the trial. The Snowflake share is Enterprise only.

Licence and attribution travel with every pull, in the `X-Eolas-*` response headers or the JSON `?envelope=1` wrapper. See [Getting started](quickstart.md#5-attribution-and-provenance).

If you work with New Zealand economic, demographic or geospatial data, eolas gets it into pandas, dplyr or SQL so you do not have to keep the pipelines running.

---

## Choose your language

=== "Python"

    ```bash
    pip install eolas-data
    ```

    ```python
    from eolas_data import Client

    client = Client("your_eolas_key")

    # Source-specific helpers. nz_cpi is the OECD annual percent change.
    df = client.oecd("nz_cpi", start="2020-01-01")
    df = client.oecd("nz_gdp_growth")

    # It's a pandas DataFrame. Plot, filter, or join as you like.
    df.plot(x="date", y="value", title="NZ CPI inflation")
    ```

=== "R"

    ```r
    install.packages("eolas", repos = c("https://phildonovan.r-universe.dev", "https://cloud.r-project.org"))
    ```

    ```r
    library(eolas)

    eolas_key("your_eolas_key")

    # Source-specific helpers. nz_cpi is the OECD annual percent change.
    df <- eolas_get_oecd("nz_cpi", start = "2020-01-01")

    # It's a data frame. Plot with ggplot2, or pipe with dplyr.
    library(ggplot2)
    ggplot(df, aes(date, value)) + geom_line()
    ```

=== "CLI"

    ```bash
    pip install eolas-data[cli]
    eolas auth set-key                       # one-time
    ```

    ```bash
    # Browse, fetch, schedule, integrate — all from the shell
    eolas datasets list --search cpi
    eolas get nz_cpi --start 2020-01-01 --format csv > cpi.csv
    eolas schedule add nz_cpi --daily --out ~/data/cpi.csv
    eolas integrate meltano --datasets nz_cpi,nz_gdp_growth    # Enterprise
    ```

    Same install on Linux, macOS, and Windows. Pipes cleanly into `jq`, `csvkit`, your spreadsheet, etc.

---

## What's in the API?

| Category | Examples |
|---|---|
| Macroeconomics | CPI, GDP growth, unemployment, interest rates |
| Labour & Earnings | Employment, wages, gender pay gap |
| Business & Enterprise | Firm counts, births/deaths, industry breakdowns |
| Population | Resident population by age, sex, ethnicity, region |
| Justice & Social | Charges, convictions, household expenditure |
| Fiscal | Government spending, revenue, debt, NZ Super Fund |
| Geospatial | Land parcels, roads, addresses, territorial authorities |

Data is sourced from **Stats NZ**, the **OECD**, **NZ Treasury**, **RBNZ**, **LINZ**, **MBIE**, **Waka Kotahi (NZTA)**, **MSD**, **NZ Police / MoJ**, **ACC**, **Education Counts**, **WorkSafe NZ**, **Auckland Council**, **Auckland Transport**, **DOC**, **Co-Lab Waikato**, **ECan / Canterbury**, **Charities Services**, **Immigration NZ**, **EECA**, **Manaaki Whenua / LRIS**, and 10 regional & district council clusters. Refreshed daily to quarterly depending on source — [live freshness](https://eolas.nz/status) · [data changelog](https://eolas.nz/data/changelog) · [Enterprise SLA](sla.md).

---

## Get an API key

Every new account starts with a [14-day Pro trial](https://eolas.nz/pricing) — no card required, and it ends automatically. [Get your key →](https://eolas.nz/signup)

| Plan | Price | Requests | Rows per request | Includes |
|---|---|---|---|---|
| Pro trial | 14 days free | Up to 1,000 | Up to 50,000 | JSON, CSV, Arrow, and Parquet. No bulk downloads, no `/changes` feed, no Snowflake share. |
| Pro | NZD $49 / mo | Unlimited | Unlimited | JSON and CSV, fresh bulk snapshots (Parquet, CSV, GeoParquet), email support. For one person. |
| Team | NZD $39 / seat / mo | Unlimited | Unlimited | Everything in Pro. 2-seat minimum. Shared team workspace, one bill. |
| Enterprise | Custom | Unlimited | Unlimited | Snowflake data share, SLA and dedicated support, custom datasets, invoiced billing. Everything in Pro. |

Prices are in NZD and include 15% GST where applicable. A request is a successful call to `/v1/datasets/<name>/data`; metadata calls and previews do not count. After the trial, dataset metadata stays available and data calls stop until you subscribe.

[View pricing →](https://eolas.nz/pricing)
