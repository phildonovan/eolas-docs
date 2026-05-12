# WorkSafe NZ data via eolas

[WorkSafe NZ](https://www.worksafe.govt.nz) is the regulator for workplace health and safety in New Zealand. It investigates incidents, conducts proactive assessments, and publishes detailed statistics on fatalities, injuries, and enforcement activities. eolas serves **8 datasets** from WorkSafe.

If you're doing occupational health research, industry-safety analysis, or compliance / consultancy work — WorkSafe is the source.

For *insurance claims* on workplace injuries (the cost side), see [ACC](acc.md). WorkSafe covers the regulator/enforcement perspective; ACC covers the claim/treatment perspective.

---

## What's in the catalogue

### Outcomes — injuries + fatalities

| Dataset | Description |
|---|---|
| `worksafe_fatalities` | Worker + member-of-public fatalities recorded by WorkSafe since 2011, broken down by industry + region. |
| `worksafe_injuries_serious_harm` | Serious harm injury notifications received by WorkSafe, broken down by industry. |
| `worksafe_injuries_week_away` | Injuries leading to a week+ off work. |
| `worksafe_incidents` | Notifiable incidents reported since 2014 — broader than serious-harm injuries. |

### Regulator activity

| Dataset | Description |
|---|---|
| `worksafe_assessments` | WorkSafe proactive workplace assessments — by industry + region. |
| `worksafe_enforcement` | Enforcement activities — improvement notices, prohibition notices, infringements. |
| `worksafe_investigations` | Investigations opened, by industry + region + classification. |
| `worksafe_concerns` | Concerns reported to WorkSafe by workers + the public. |

---

## Refresh schedule

Monthly. WorkSafe publishes most series quarterly; our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("worksafe_fatalities")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All WorkSafe data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: WorkSafe New Zealand, served via eolas (eolas.fyi). CC-BY 4.0."*

A privacy note: data is aggregated. Specific incident details (location, persons involved) are not published in the open dataset — those require formal information requests.

---

## Common patterns

### Workplace fatality trend by industry

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    fat = client.worksafe("worksafe_fatalities", start="2015-01-01")
    by_year_ind = fat.groupby(["year", "industry"])["count"].sum().reset_index()

    top_industries = fat.groupby("industry")["count"].sum().nlargest(5).index
    pivot = by_year_ind[by_year_ind["industry"].isin(top_industries)].pivot(
        index="year", columns="industry", values="count"
    )
    pivot.plot(title="WorkSafe fatalities — top 5 industries", figsize=(10, 6))
    plt.show()
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    fat <- eolas_get_worksafe("worksafe_fatalities", start = "2015-01-01")
    top5 <- fat |> group_by(industry) |> summarise(n = sum(count)) |> top_n(5, n) |> pull(industry)
    fat_top <- fat |> filter(industry %in% top5)
    ggplot(fat_top, aes(year, count, colour = industry)) + geom_line()
    ```

### Serious-harm rate by industry size

```python
sh = client.worksafe("worksafe_injuries_serious_harm")
# Combine with employment counts from Stats NZ to compute rate per 1000 workers
emp = client.statsnz("leed_q_measures_industry")
# Join on industry, compute rate, etc.
```

### Enforcement activity over time

```python
enf = client.worksafe("worksafe_enforcement", start="2018-01-01")
by_type = enf.groupby(["year", "notice_type"])["count"].sum().reset_index()
pivot = by_type.pivot(index="year", columns="notice_type", values="count")
pivot.plot(title="WorkSafe enforcement notices by type")
```

---

## Source-specific notes

- **Fatalities count "worker" + "member of public"**: agriculture-related public fatalities (e.g. quad bikes on farms) are counted as workplace-related. Check the breakdown column if doing pure worker-fatality analysis.
- **HSWA 2015 boundary**: the Health and Safety at Work Act 2015 replaced the previous HSE Act. Notification thresholds changed in 2015-16. Pre-2015 incidents may not be directly comparable to post-2015.
- **Industry classification**: WorkSafe uses ANZSIC industry codes — see [stats.govt.nz/methods/anzsic-2006](https://www.stats.govt.nz/methods/anzsic-2006-classifications-and-statistics-page) for the full taxonomy.
- **"Notifiable" criteria**: WorkSafe defines notifiable death, illness, injury, and incident in section 23 of HSWA. Not every workplace accident triggers a notification.
- **Investigations subset of incidents**: an incident is notified; an investigation is opened only on a subset. Different denominators.
- **Mining + forestry historically high-rate**: per FTE, these industries consistently top fatality rates. Construction is high-volume but typically lower per-worker rate.

---

## Where to find more

- **WorkSafe datasets on eolas**: [eolas.fyi/datasets?source=WorkSafe+NZ](https://eolas.fyi/datasets?source=WorkSafe%20NZ)
- **WorkSafe Open Data**: [data.worksafe.govt.nz](https://data.worksafe.govt.nz)
- **HSWA 2015**: [www.worksafe.govt.nz/laws-and-regulations/acts](https://www.worksafe.govt.nz/laws-and-regulations/acts)

## Related

- [ACC source guide](acc.md) — for the claims / treatment side of workplace injuries
- [Stats NZ source guide](statsnz.md) — for industry employment denominators (BDS + LEED)
- [Examples](../examples/index.md) — worked code recipes
