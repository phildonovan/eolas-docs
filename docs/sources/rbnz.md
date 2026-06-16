# RBNZ data via eolas

The [Reserve Bank of New Zealand](https://www.rbnz.govt.nz/statistics) publishes the canonical NZ money-and-banking statistics. eolas serves **32 datasets** from RBNZ, organised by the RBNZ's own letter-numbered table system (`B1`, `B2`, …, `C` series, `M` series).

If you do anything involving mortgages, exchange rates, NZ monetary aggregates, or balance-of-payments — RBNZ is the source.

---

## What's in the catalogue

The 32 datasets cover RBNZ's statistical-release tables. The naming convention is `rbnz_<table_code>_<topic>`, e.g. `rbnz_b1_exchange_rates_daily`.

### Interest rates

| Dataset | Description |
|---|---|
| `rbnz_b1_exchange_rates_daily` | Daily TWI and bilateral exchange rates (NZD vs major currencies). |
| `rbnz_b1_exchange_rates_monthly` | Monthly averages of the same. |
| `rbnz_b2_wholesale_rates_daily` | Wholesale rates, end-of-day close — OCR, bank bills, government bond yields, swap rates. |
| `rbnz_b2_wholesale_rates_monthly` | Monthly averages of the same (close basis). |
| `rbnz_b3_retail_rates` | Retail / household rates (term deposits, lending). |
| `rbnz_b20_mortgage_rates` | Mortgage rates by fixed term and lender. |

### Money supply, credit, banking

| Dataset | Description |
|---|---|
| `rbnz_c5_credit_extended` | Credit extended to households, business, and agriculture. |
| `rbnz_c31_new_mortgage_lending` | New mortgage lending by LVR band and borrower type — useful for housing-market analysis. |
| `rbnz_c33_mortgage_by_purpose` | New mortgage lending by purpose (first-home, investor, owner-occupier). |
| `rbnz_c40_monetary_aggregates` | New residential mortgage lending by debt-to-income (DTI) band. *(The `monetary_aggregates` id is a historical misnomer — the content is DTI lending.)* |
| `rbnz_c71_residential_mortgage_lending` | Residential mortgage lending by rate type (fixed/floating mix). |

### Macro + external

| Dataset | Description |
|---|---|
| `rbnz_m7_balance_of_payments` | Current account, capital account, NIIP. |
| `rbnz_m8_overseas_trade` | Goods and services exports / imports. |
| `rbnz_m9_labour_market` | Employment, wages, productivity proxies (RBNZ's view; differs slightly from Stats NZ). |

For the full list, browse [eolas.fyi/datasets?source=RBNZ](https://eolas.fyi/datasets?source=RBNZ).

---

## Refresh schedule

Daily for the rate/FX tables (B1 exchange rates, B2 wholesale rates), daily checks with monthly/quarterly source cadence for the rest (the pipeline's change detection skips unchanged source files). One exception: `rbnz_m13_inflation_expectations` is **archived** — RBNZ discontinued its source file in June 2022, so the dataset is the 1995–2022 historical series and no longer updates.

---

## License

All RBNZ statistical data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)** per the [RBNZ Open Data policy](https://www.rbnz.govt.nz/-/media/project/sites/rbnz/files/about-us/copyright-statement.pdf). Commercial use is fine; attribution is required.

Recommended attribution: *"Source: Reserve Bank of New Zealand, via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### OCR + 90-day rate

The two interest rates every analyst tracks:

=== "Python"

    ```python
    import pandas as pd
    import matplotlib.pyplot as plt

    rates = client.rbnz("rbnz_b2_wholesale_rates_daily", start="2018-01-01")

    # Tables are WIDE: one column per series, snake_cased from RBNZ's headers.
    rates.plot(x="date",
               y=["cash_rate_official_cash_rate_ocr", "bank_bill_yields_90_days"],
               figsize=(10, 4), title="OCR vs 90-day bank bill")
    plt.show()
    ```

=== "R"

    ```r
    library(tidyr)
    library(ggplot2)

    rates <- eolas_get_rbnz("rbnz_b2_wholesale_rates_daily", start = "2018-01-01")

    # Tables are wide: one column per series, snake_cased from RBNZ's headers.
    ggplot(rates, aes(date)) +
      geom_line(aes(y = cash_rate_official_cash_rate_ocr, colour = "OCR")) +
      geom_line(aes(y = bank_bill_yields_90_days, colour = "90-day")) +
      labs(y = "Rate (%)", colour = NULL)
    ```

### Mortgage rates by term

=== "Python"

    ```python
    mort = client.rbnz("rbnz_b20_mortgage_rates", start="2020-01-01")
    # One column per fixed term (wide format)
    mort.plot(x="date",
              y="new_standard_residential_mortgage_interest_rates_average_pct_end_of_month_2_years",
              title="NZ 2-year fixed mortgage rate")
    ```

### LVR composition of new lending

=== "Python"

    ```python
    lvr = client.rbnz("rbnz_c31_new_mortgage_lending", start="2018-01-01")
    # High-LVR (>80%) share of all new lending — the RBNZ's macroprudential target
    lvr["high_lvr_share_pct"] = (
        lvr["higher_than_80_pct_lvr_lending_b1_all_borrower_types_b2_b3_b4_b5"]
        / lvr["total_lending_a1_all_borrower_types_a2_a3_a4_a5"] * 100
    )
    lvr.plot(x="date", y="high_lvr_share_pct",
             title="High-LVR share of new mortgage lending (%)")
    ```

---

## Pipeline use

RBNZ datasets are full-snapshot — each RBNZ release replaces the whole table. Most RBNZ tables are small (exchange-rate series are a few hundred KB; the larger balance-sheet tables top out around 5 MB), so full re-downloads are fast.

Use `sync_bulk` / `eolas_sync_bulk` to keep a local file fresh — it issues a lightweight HEAD check and only re-downloads when the snapshot has changed. In weeks where RBNZ hasn't published a new release, the call returns "unchanged" and transfers zero bytes.

=== "Python"

    ```python
    result = client.sync_bulk("rbnz_b1_exchange_rates_daily",
                              path="/data/rbnz_b1_exchange_rates_daily.parquet")
    print(result.status)  # "downloaded" (first run) or "unchanged"

    import pandas as pd
    df = pd.read_parquet("/data/rbnz_b1_exchange_rates_daily.parquet")
    ```

=== "R"

    ```r
    result <- eolas_sync_bulk("rbnz_b1_exchange_rates_daily",
                              path = "/data/rbnz_b1_exchange_rates_daily.parquet")
    result$status  # "downloaded" or "unchanged"
    ```

=== "CLI"

    ```bash
    eolas sync rbnz_b1_exchange_rates_daily --out /data/rbnz_b1_exchange_rates_daily.parquet
    # → downloaded (first run) or unchanged (snapshot 5503437…)
    ```

See the [Bulk downloads](../bulk-downloads.md) guide for cron and Airflow recipes.

---

## Source-specific notes

- **Naming**: dataset names follow `rbnz_<rbnz_table_code>_<topic>` so they cross-reference cleanly to RBNZ's own [Statistics page](https://www.rbnz.govt.nz/statistics) — if you read a "B2" release on RBNZ's website, the eolas dataset is `rbnz_b2_*`.
- **Wide format**: tables are one row per date with one column per series, snake_cased from RBNZ's multi-row Excel headers (e.g. `cash_rate_official_cash_rate_ocr`). No pivoting needed for charting; use `df.melt()` / `tidyr::pivot_longer()` if you want long format.
- **Cloudflare**: RBNZ's site is Cloudflare-protected. Our pipeline uses residential-proxy fallback to fetch reliably; you don't see this — just clean data. If you're scraping RBNZ directly without proxies you'll see 403s from Fargate-IP-range addresses.
- **Recent retirement**: RBNZ retired 8 legacy tables in May 2026 (404s on the source). We removed those from our schedule rather than report broken pipelines; if you have older code referencing them, the dataset names will 404 from us too.

---

## Where to find more

- **RBNZ datasets on eolas**: [eolas.fyi/datasets?source=RBNZ](https://eolas.fyi/datasets?source=RBNZ)
- **RBNZ's own statistics page**: [www.rbnz.govt.nz/statistics](https://www.rbnz.govt.nz/statistics) — original Excel tables, methodology notes
- **RBNZ OCR decisions**: [www.rbnz.govt.nz/monetary-policy/about-monetary-policy/ocr-decisions](https://www.rbnz.govt.nz/monetary-policy/about-monetary-policy/ocr-decisions)

## Related

- [Stats NZ source guide](statsnz.md) — for the labour, GDP, BOP series Stats NZ publishes (overlaps with RBNZ's M-series)
- [Examples](../examples/index.md) — worked code recipes
