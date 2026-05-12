# NZ Police / MoJ data via eolas

eolas serves **5 datasets** from [NZ Police](https://www.police.govt.nz) + the [Ministry of Justice](https://www.justice.govt.nz) — the canonical sources for road policing infringements and court charges in New Zealand.

If you're doing road-safety analysis, alcohol-policy research, court / criminal-justice work, or location-specific policing studies — this is the source.

For *crashes* (the consequence side), use [NZTA / Waka Kotahi](nzta.md) — they own CAS crash data. Police data covers *enforcement actions* (offences detected, charges filed).

---

## What's in the catalogue

### Road policing — NZ Police

| Dataset | Description |
|---|---|
| `police_road_offences` | Monthly counts of road policing infringements by police district + area, 2009+. |
| `police_camera_offences` | Monthly counts of camera-issued traffic offences by site location, 2009+. |
| `police_breath_tests` | Quarterly passive + screening breath alcohol tests conducted by NZ Police district. |

### Court charges — Ministry of Justice

| Dataset | Description |
|---|---|
| `moj_charges_by_offence` | Annual count of finalised court charges in NZ broken down by ANZSOC offence code. |
| `moj_people_charged` | Annual count of distinct people with finalised court charges (defendant counts, not charge counts). |

---

## Refresh schedule

Quarterly. Police data updates monthly at source; MoJ data annually (calendar year basis, published mid-year following). Our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("police_road_offences")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Police + MoJ data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: NZ Police"* or *"Source: Ministry of Justice"*, served via eolas (eolas.fyi). CC-BY 4.0.

A privacy note: data is aggregated. Small-cell suppression applies where individual case identification might be possible (typically counts ≤4 in specific demographic / location combinations).

---

## Common patterns

### Road-policing infringement trend by district

=== "Python"

    ```python
    rp = client.police_moj("police_road_offences", start="2015-01-01")
    # By district + month
    by_dist = rp.groupby(["date", "police_district"])["count"].sum().reset_index()
    pivot = by_dist.pivot(index="date", columns="police_district", values="count")
    pivot.plot(title="Road policing infringements by district", figsize=(12, 6))
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    rp <- eolas_get_police_moj("police_road_offences", start = "2015-01-01")
    rp_by <- rp |> group_by(date, police_district) |> summarise(count = sum(count))
    ggplot(rp_by, aes(date, count, colour = police_district)) + geom_line()
    ```

### Camera offences by site

```python
cam = client.police_moj("police_camera_offences", start="2020-01-01")
# Top 10 sites by total camera-issued offences
top = cam.groupby("site_location")["count"].sum().sort_values(ascending=False).head(10)
print(top)
```

### Breath-test rate

```python
bt = client.police_moj("police_breath_tests", start="2018-01-01")
# Positive-detection rate by quarter
bt["positive_rate"] = bt["positive_results"] / bt["total_tests"]
by_q = bt.groupby("date")["positive_rate"].mean()
by_q.plot(title="Positive breath-test detection rate")
```

### MoJ charges by offence category

```python
charges = client.police_moj("moj_charges_by_offence")
# Top offence categories most recent year
latest = charges[charges["year"] == charges["year"].max()]
print(latest.groupby("anzsoc_division")["charges"].sum().sort_values(ascending=False).head(10))
```

---

## Source-specific notes

- **Infringements ≠ convictions ≠ crashes**: a road-policing infringement is an offence *detected* by Police (driver issued a notice). It may or may not be paid / contested / withdrawn. For *convictions*, use MoJ data. For *crashes*, use NZTA CAS. Don't confuse the three.
- **Police districts vs council areas**: NZ Police has 12 districts that don't align with regional or territorial council boundaries. Some districts (e.g. Counties Manukau) cover parts of multiple regions.
- **Camera-offences scope**: includes red-light + speed cameras only. Some camera-issued offences (e.g. mobile cameras at specific events) may not be reflected.
- **Breath-test methodology change**: pre-2020 vs post-2020 sampling methodology differs slightly. Compare cautiously across the boundary.
- **ANZSOC offence codes**: Australian and New Zealand Standard Offence Classification — see [stats.govt.nz/methods/anzsoc](https://www.stats.govt.nz/methods/anzsoc-2011) for the full taxonomy.
- **Defendant counts ≠ unique people**: `moj_people_charged` is unique people per year. Someone charged in multiple years counts in each year separately.
- **Court charges are "finalised"**: i.e. the case has reached a final disposition (guilty / not guilty / withdrawn / etc.). Active / unresolved cases aren't in the data.

---

## Where to find more

- **Datasets on eolas**: [eolas.fyi/datasets?source=NZ+Police+%2F+MoJ](https://eolas.fyi/datasets?source=NZ%20Police%20%2F%20MoJ)
- **NZ Police data**: [www.police.govt.nz/about-us/publications-statistics/data-and-statistics](https://www.police.govt.nz/about-us/publications-statistics/data-and-statistics)
- **MoJ statistics**: [www.justice.govt.nz/justice-sector-policy/research-data/justice-statistics](https://www.justice.govt.nz/justice-sector-policy/research-data/justice-statistics)

## Related

- [NZTA / Waka Kotahi](nzta.md) — for road crashes (CAS) data
- [Stats NZ source guide](statsnz.md) — for population denominators + justice statistics
- [Examples](../examples/index.md) — worked code recipes
