# Stats NZ data via eolas

[Statistics New Zealand](https://www.stats.govt.nz) is the national statistical agency. eolas serves **415 datasets** from Stats NZ — the largest single source in the catalogue — covering everything from quarterly CPI prints to 2023-vintage census meshblock boundaries.

This page is the orientation guide. For specific datasets, browse [eolas.fyi/datasets?source=Stats+NZ](https://eolas.fyi/datasets?source=Stats%20NZ).

---

## What's in the catalogue

Stats NZ datasets fall into seven broad categories. Counts are approximate; check the [live API](https://api.eolas.fyi/v1/datasets) for current totals.

### Macroeconomic indicators

CPI, GDP, unemployment, balance-of-payments. Quarterly series for most. See also the [OECD source guide](oecd.md) — OECD provides the same headline indicators with international comparability.

```python
df = client.statsnz("nz_cpi", start="2020-01-01")
df = client.statsnz("nz_gdp_production_annual")
```

### Business demography (BDS)

Enterprise counts, business births and deaths, industry breakdowns, geographic units by region and size. ~30 datasets prefixed `bds_`.

```python
df = client.statsnz("bds_enterprises_industry_size")
df = client.statsnz("bds_geographic_units_births_deaths")
```

### Population estimates and projections

National + sub-national estimated resident population, projections to 2048, by age / sex / ethnicity / Māori-descent. Prefixed `popes_` (estimates) and `poppr_` (projections).

```python
df = client.statsnz("popes_subnational_by_age")
df = client.statsnz("poppr_national_by_age_sex_to_2048")
```

### Productivity and earnings

Labour productivity, multifactor productivity, LEED (linked employer-employee data), wages by industry / occupation / region.

```python
df = client.statsnz("prd_labour_productivity")
df = client.statsnz("leed_q_earnings_industry")
```

### Justice and social

Charges, convictions, youth justice, household expenditure, household income. Prefixed `jus_`, `hes_` (household expenditure), `inc_` (income).

```python
df = client.statsnz("jus_charges_by_offence_type")
df = client.statsnz("hes_household_spending_by_category")
```

### Iwi statistics (2018 census)

Iwi affiliation, iwi grouping counts for the Māori-descent population. 20+ datasets prefixed `iwi18_`. Note: 2023 census iwi frame not yet published; 2018 is current.

```python
df = client.statsnz("iwi18_population_by_iwi")
```

### Geospatial boundaries

Census meshblocks, statistical areas (SA1/SA2/SA3), territorial authorities, regional councils, wards, urban areas — for 2013, 2018, and 2023 vintages. All available as `sf` / `GeoDataFrame` when the geo extras are installed.

```python
mb = client.statsnz_geo("nz_meshblock_2023", as_sf=True)
ta = client.statsnz_geo("nz_territorial_authority_2023", as_sf=True)
```

Boundary vintages matter — see the [vintaged columns convention](https://github.com/phildonovan/eolas/blob/main/docs/data-conventions.md#13-vintaged-concepts-carry-the-year-in-the-column-name) for joining historical census data to current geographies.

---

## Refresh schedule

Most Stats NZ pipelines run **weekly, Wednesday morning NZ time**. Stats NZ itself publishes on its own schedule — CPI is quarterly, business demography annual, population estimates quarterly. Our refresh fires once a week regardless; if the upstream hasn't changed, the data is identical to last week.

You can check the freshness of any specific dataset via the metadata endpoint:

```python
meta = client.info("nz_cpi")
meta["last_refreshed_at"]        # our last pull
meta["source_last_modified_at"]  # when Stats NZ last touched the file (where capturable)
```

---

## License

All Stats NZ data is published under **[Creative Commons Attribution 4.0 (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**. You can use it commercially, derive from it, and redistribute — with attribution. eolas serves the data unchanged; attribution requirements transfer to you when you redistribute.

Recommended attribution: *"Source: Stats NZ, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### CPI over time

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    cpi = client.statsnz("nz_cpi", start="2010-01-01")
    cpi.plot(x="date", y="value", title="NZ CPI", figsize=(10, 4))
    plt.show()
    ```

=== "R"

    ```r
    library(ggplot2)

    cpi <- eolas_get_statsnz("nz_cpi", start = "2010-01-01")
    ggplot(cpi, aes(date, value)) +
      geom_line() +
      labs(title = "NZ CPI", y = "Index")
    ```

### Census boundary + value join

The classic geo-demographic pattern: load boundaries, join your own data:

=== "Python"

    ```python
    # 2023 SA2 boundaries (about 2,000 polygons, fits in Free tier)
    sa2 = client.statsnz_geo("nz_sa2_2023", as_sf=True)

    # Your own analysis data (with sa2_code_2023 column)
    import pandas as pd
    survey = pd.read_csv("my_survey.csv")

    merged = sa2.merge(survey, on="sa2_code_2023")
    merged.plot(column="my_metric", legend=True, cmap="viridis")
    ```

=== "R"

    ```r
    library(sf)
    library(ggplot2)

    sa2 <- eolas_get_statsnz_geo("nz_sa2_2023", as_sf = TRUE)
    survey <- read.csv("my_survey.csv")

    merged <- merge(sa2, survey, by = "sa2_code_2023")
    ggplot(merged) + geom_sf(aes(fill = my_metric))
    ```

### Discovering Stats NZ datasets

```bash
# CLI
eolas datasets list --source "Stats NZ" --search population

# Python
[d for d in client.list("Stats NZ") if "population" in d["name"]]

# R
sn <- eolas_list_statsnz()
sn[grepl("population", sn$name), ]
```

---

## Source-specific notes

- **SDMX origin**: most Stats NZ time-series come from their SDMX API. Multi-dimensional series (e.g. CPI by quarter × group) are flattened into a long-format `(date, period, value, ...)` table. The `period` column carries the original SDMX period code (e.g. `2024Q1`).
- **Vintage-suffixed columns**: any geospatial column drawn from the 2023 census frame carries `_2023` (e.g. `meshblock_id_2023`, `sa2_code_2023`). 2018-frame columns carry `_2018`. Don't assume codes match across vintages — boundaries are redrawn every 5 years.
- **Suppressed counts**: for privacy, Stats NZ rounds many small-count cells to base-3 and suppresses cells below threshold (typically `<6`). These appear as `null` with a companion `_suppressed=true` flag in the response.
- **Provisional vs final**: some boundary tables exist in both forms (e.g. `nz_ward_2025_v2_provisional` and `nz_ward_2025`). The provisional version is usually the working draft Stats NZ released for public consultation; the un-suffixed version is the final.

---

## Where to find more

- **All Stats NZ datasets on eolas**: [eolas.fyi/datasets?source=Stats+NZ](https://eolas.fyi/datasets?source=Stats%20NZ)
- **Stats NZ's own data portal**: [www.stats.govt.nz](https://www.stats.govt.nz) — SDMX API, downloads, methodology
- **Stats NZ Geospatial (Datafinder)**: [datafinder.stats.govt.nz](https://datafinder.stats.govt.nz) — the WFS/Koordinates source for our boundary tables
- **Open data licence summary**: [data.govt.nz/about/open-data-nzgoal](https://data.govt.nz/about/open-data-nzgoal)

## Related

- [OECD source guide](oecd.md) — international-comparable indicators
- [Examples](../examples/index.md) — worked code recipes
- [Authentication](../authentication.md) — how to set your API key
