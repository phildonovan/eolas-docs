# MSD data via eolas

The [Ministry of Social Development](https://www.msd.govt.nz) (MSD) administers New Zealand's working-age benefit system, NZ Superannuation, the housing register, and student support. eolas serves **12 datasets** from MSD — the canonical official statistics on who's receiving what kind of support.

If you're doing labour-market analysis, social-policy research, housing-affordability work, or fiscal modelling — MSD is the source.

---

## What's in the catalogue

### Working-age benefits

| Dataset | Description |
|---|---|
| `msd_main_benefit_summary` | Quarterly count of recipients by benefit type (Jobseeker Support, Sole Parent, Supported Living, etc.). |
| `msd_main_benefit_characteristics` | Same quarterly recipients broken down by gender, age, ethnicity, region. |
| `msd_benefit_by_ta` | Quarterly recipient counts by territorial authority. |
| `msd_benefit_grants` | New benefit grants (flow, not stock) by quarter + benefit type. |
| `msd_benefit_cancels` | Benefit cancellations by quarter + reason. |
| `msd_benefit_sanctions` | Quarterly count of sanctions imposed by benefit type, 2021+. |

### NZ Superannuation + Veteran's Pension

| Dataset | Description |
|---|---|
| `msd_nzs_vp_summary` | Quarterly count of NZS + Veteran's Pension recipients. |
| `msd_nzs_recipient_characteristics` | NZS recipients broken down by gender, age, ethnicity. |

### Housing

| Dataset | Description |
|---|---|
| `msd_housing_register_priority` | Quarterly count of public-housing applicants by priority band (A / B). |
| `msd_housing_register_ta` | Same housing register by territorial authority. |

### Student support

| Dataset | Description |
|---|---|
| `msd_student_allowance` | Annual Student Allowance recipients, amounts, averages by category. |
| `msd_student_loan` | Annual Student Loan counts + amounts by loan component (fees, course costs, living costs). |

---

## Refresh schedule

Weekly, Wednesday morning NZ time. MSD publishes most series quarterly; student support is annual (calendar year, after the academic year closes).

```python
meta = client.info("msd_main_benefit_summary")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All MSD data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Ministry of Social Development, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Jobseeker Support trend through cycles

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    bs = client.msd("msd_main_benefit_summary", start="2015-01-01")
    jss = bs[bs["benefit_type"] == "Jobseeker Support"]
    jss.plot(x="date", y="count", title="Jobseeker Support recipients")
    plt.show()
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    bs <- eolas_get_msd("msd_main_benefit_summary", start = "2015-01-01")
    jss <- bs |> filter(benefit_type == "Jobseeker Support")
    ggplot(jss, aes(date, count)) + geom_line() +
      labs(title = "Jobseeker Support recipients")
    ```

### Housing register pressure by TA

```python
hr = client.msd("msd_housing_register_ta", start="2018-01-01")
# Top 10 TAs by housing register count, latest quarter
latest = hr[hr["date"] == hr["date"].max()]
top = latest.groupby("ta_name")["count"].sum().sort_values(ascending=False).head(10)
print(top)
```

### NZS as share of working-age population

```python
nzs = client.msd("msd_nzs_vp_summary")
nzs_total = nzs.groupby("date")["count"].sum()
# Compare to total population from Stats NZ
pop = client.statsnz("popes_erp_components")
combined = pop.merge(nzs_total.rename("nzs"), on="date")
combined["nzs_share"] = combined["nzs"] / combined["population"]
combined.plot(x="date", y="nzs_share", title="NZS recipients / total population")
```

---

## Source-specific notes

- **Working-age = 18-64**: the "main benefit" series excludes NZS (65+) and student support. Use the appropriate series for your question.
- **Sanctions data starts 2021**: prior years don't have a comparable sanctions series. Don't read pre-2021 zeros as actual zero sanctions.
- **TA boundaries vary by vintage**: the `ta_name` field in `msd_*_by_ta` series uses TA boundaries as of the publication quarter. Pre-2017 data uses the pre-amalgamation Auckland names; recent uses single Auckland Council.
- **Population denominators**: many ratios you'll calculate (e.g. benefit recipients per 1000 working-age) need a denominator from Stats NZ — use the `popes_*` series with matched dates.
- **NZS includes Veteran's Pension**: `msd_nzs_vp_summary` is the combined total. They're administered together but legislated separately. For NZS-only analysis, check the recipient_characteristics breakdown.
- **Sole Parent Support previously called "Domestic Purposes Benefit (DPB)"**: the 2013 reforms renamed and restructured benefits. Historical data is conformed forward where comparable, but cross-2013 series should be read with care.

---

## Where to find more

- **MSD datasets on eolas**: [eolas.fyi/datasets?source=MSD](https://eolas.fyi/datasets?source=MSD)
- **MSD Open Data Portal**: [www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/index.html](https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/index.html)
- **Benefit-fact-sheets** (regular reports): [www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/benefit/index.html](https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/benefit/index.html)

## Related

- [Stats NZ source guide](statsnz.md) — for population denominators + LEED labour-market data
- [NZ Treasury source guide](treasury.md) — for fiscal cost of the benefit system (Crown Financial Statements)
- [Examples](../examples/index.md) — worked code recipes
