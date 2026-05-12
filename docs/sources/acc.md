# ACC data via eolas

The [Accident Compensation Corporation](https://www.acc.co.nz) (ACC) administers New Zealand's no-fault accident insurance scheme. ACC publishes detailed claim statistics — broken down by injury type, sport / activity, age cohort, region, and outcome. eolas serves **73 datasets** from ACC — the largest single source after Stats NZ.

If you're doing injury-prevention research, healthcare-cost analysis, sport-safety studies, occupational health research, or actuarial work — ACC is the source.

---

## What's in the catalogue

ACC publishes thematically rather than as one giant table. Each dataset typically covers a specific injury type, activity, or cohort. Themes include:

### Sport + recreation injuries

| Examples |
|---|
| `acc_acl_injuries` (anterior cruciate ligament) |
| `acc_achilles_tendon_ruptures` |
| `acc_climbing_related_claims_lodged_between_1_january_2018_and_31_december_2022` |
| `acc_cycling_injury_data` |
| `acc_cricket_related_upper_limb_injuries` |
| `acc_skiing_and_snowboarding_injuries` |

### Vehicle-related injuries

| Examples |
|---|
| `acc_e_scooter_injuries` |
| `acc_motorcycle_injuries` |
| `acc_pedestrian_injury_data` |

### Workplace + sector injuries

| Examples |
|---|
| `acc_education_sector_claims` |
| `acc_health_and_social_assistance_sector_claims` |
| `acc_construction_sector_claims` |
| `acc_chainsaw_related_injuries` |

### Body-region injuries

| Examples |
|---|
| `acc_concussion_tbi_data_update` (traumatic brain injury) |
| `acc_eye_injuries` |
| `acc_carpal_tunnel_injuries` |
| `acc_cubital_tunnel_syndrome_claims` |

### Cohort + demographic breakdowns

| Examples |
|---|
| `acc_claims_for_children_and_teenagers` |
| `acc_falls_dataset` (elderly falls — high cost cohort) |
| `acc_falls_dataset_update` |

### Operations + service data

| Examples |
|---|
| `acc_elective_surgery_data` (ACC-funded surgeries) |
| `acc_diagnostic_imaging_acc_claims_by_modality` |

Browse the full list: [eolas.fyi/datasets?source=ACC](https://eolas.fyi/datasets?source=ACC).

---

## Refresh schedule

Monthly. ACC publishes most datasets quarterly or annually; our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("acc_acl_injuries")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All ACC data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)** via the [ACC OIA + Open Data Programme](https://www.acc.co.nz/about-us/statistics/open-data-programme). Commercial use is fine; attribution required.

Recommended attribution: *"Source: Accident Compensation Corporation, served via eolas (eolas.fyi). CC-BY 4.0."*

A privacy note: ACC publishes aggregate counts, not individual claims. Small-cell suppression applies to cells below threshold (typically ≤4 claims) — these appear as `null` with a suppression flag where present.

---

## Common patterns

### E-scooter injury trend

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    es = client.acc("acc_e_scooter_injuries")
    # Most ACC datasets have columns: year, region, injury_type, count, cost
    by_year = es.groupby("year")["count"].sum()
    by_year.plot(title="E-scooter injuries (ACC claims)")
    plt.show()
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    es <- eolas_get_acc("acc_e_scooter_injuries")
    by_year <- es |> group_by(year) |> summarise(count = sum(count))
    ggplot(by_year, aes(year, count)) + geom_line() +
      labs(title = "E-scooter injuries (ACC claims)")
    ```

### Falls in the elderly — the big-cost cohort

```python
falls = client.acc("acc_falls_dataset")
# Cost per claim by age band
by_age = falls.groupby("age_band").agg({"count": "sum", "total_cost": "sum"}).reset_index()
by_age["cost_per_claim"] = by_age["total_cost"] / by_age["count"]
print(by_age.sort_values("cost_per_claim", ascending=False))
```

### Sector-specific injury rate

```python
education = client.acc("acc_education_sector_claims")
# Filter to most-recent year
latest = education[education["year"] == education["year"].max()]
# By injury type
print(latest.groupby("injury_type")["count"].sum().sort_values(ascending=False).head(10))
```

---

## Source-specific notes

- **Lots of small thematic datasets**: ACC publishes per-topic rather than one giant table. To compare across themes (e.g. ACL injuries vs eye injuries) you'll need to load each dataset separately. Use the search filter on [eolas.fyi/datasets?source=ACC](https://eolas.fyi/datasets?source=ACC) to find what's there.
- **Schemas vary**: ACC datasets are published as OIA responses — each tends to follow the columns the original requestor asked for. Use `client.info(name)` to inspect schema before joining.
- **Claims ≠ injuries**: an ACC claim is one *interaction* with the scheme; a single injury can generate multiple claims (initial assessment, follow-up, surgery, rehab). Count the right unit for your analysis.
- **Costs are scheme costs, not full healthcare costs**: ACC funds part of the care (specifically the accident component). Hospital admissions, primary care, and prescriptions outside the ACC scheme aren't reflected.
- **Provisional vs final**: recent quarters are sometimes provisional and revised upward as late claims are accepted. The most-recent 2-3 quarters are usually still moving.
- **Coverage history**: ACC has been operating since 1974. Most datasets start in 2000-2010; very few have data older than that.

---

## Where to find more

- **ACC datasets on eolas**: [eolas.fyi/datasets?source=ACC](https://eolas.fyi/datasets?source=ACC)
- **ACC Open Data Programme**: [www.acc.co.nz/about-us/statistics/open-data-programme](https://www.acc.co.nz/about-us/statistics/open-data-programme)
- **ACC Annual Report** (scheme totals): [www.acc.co.nz/about-us/who-we-are/reports-and-plans](https://www.acc.co.nz/about-us/who-we-are/reports-and-plans)

## Related

- [WorkSafe NZ source guide](worksafe.md) — for workplace fatalities + serious harm (regulator side; ACC is the insurance side)
- [NZTA source guide](nzta.md) — for road crashes (CAS) data
- [Examples](../examples/index.md) — worked code recipes
