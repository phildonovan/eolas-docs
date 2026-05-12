# PHARMAC data via eolas

[Te Pātaka Whaioranga – PHARMAC](https://pharmac.govt.nz) is New Zealand's pharmaceutical management agency — it negotiates pricing and decides which medicines are funded under the public health system. eolas serves **4 datasets** from PHARMAC: the current community + hospital medicines schedules plus monthly historical snapshots back to 2011.

If you're doing pharmaceutical policy research, market access work, generic-launch tracking, or studying NZ pharmaceutical funding decisions over time — PHARMAC is the source.

---

## What's in the catalogue

| Dataset | Description |
|---|---|
| `pharmac_schedule` | Current month's community pharmaceutical schedule (CPS) — every funded community medicine, with brand, strength, formulation, subsidy, special-authority status. |
| `pharmac_schedule_history` | Monthly snapshots of the CPS from September 2010 to present (~14 years of monthly snapshots, ~840k rows). |
| `pharmac_hospital_medicines_list` | Current month's hospital medicines list (HML) — medicines funded for inpatient use. |
| `pharmac_hml_history` | Monthly snapshots of the HML from January 2011 to present. |

---

## Refresh schedule

Monthly. PHARMAC publishes both schedules monthly; our refresh runs weekly to catch new releases promptly. New schedule editions typically issue mid-month with funding changes effective from the 1st of the following month.

```python
meta = client.info("pharmac_schedule")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All PHARMAC data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Te Pātaka Whaioranga – PHARMAC, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### What's funded for a specific medicine?

=== "Python"

    ```python
    sched = client.pharmac("pharmac_schedule")
    # All funded brands for paracetamol
    para = sched[sched["chemical_name"].str.lower().str.contains("paracetamol")]
    print(para[["brand", "strength", "form_type", "subsidy"]])
    ```

=== "R"

    ```r
    library(dplyr)
    sched <- eolas_get_pharmac("pharmac_schedule")
    para <- sched |> filter(grepl("paracetamol", tolower(chemical_name)))
    print(para[, c("brand", "strength", "form_type", "subsidy")])
    ```

### When was a medicine first funded?

```python
hist = client.pharmac("pharmac_schedule_history")
# Find first appearance of "semaglutide" (Ozempic / Wegovy active ingredient)
hits = hist[hist["chemical_name"].str.lower() == "semaglutide"]
print(f"First listed: {hits['snapshot_date'].min()}")
```

### Generic-launch tracking

```python
hist = client.pharmac("pharmac_schedule_history", start="2020-01-01")
# Brands per chemical, per month — proxy for generic entry
by_month = hist.groupby(["snapshot_date", "chemical_name"])["brand"].nunique().reset_index()
# Chemicals where brand count grew
multi_brand = by_month.groupby("chemical_name")["brand"].max()
new_generics = multi_brand[multi_brand > 1].sort_values(ascending=False).head(20)
print(new_generics)
```

### Subsidy spend over time

```python
hist = client.pharmac("pharmac_schedule_history")
# Total subsidised cost by month (where unit price + quantity available)
hist["est_cost"] = hist["price_per_unit"] * hist["dispensings"]
by_month = hist.groupby("snapshot_date")["est_cost"].sum()
by_month.plot(title="Estimated CPS subsidy spend by month")
```

---

## Source-specific notes

- **CPS vs HML**: the Community Pharmaceutical Schedule covers medicines dispensed in pharmacies (subsidised + special-authority); the Hospital Medicines List covers medicines used in hospitals. Funding rules differ; both schedules update independently.
- **Snapshot history is a goldmine**: ~14 years of monthly snapshots lets you see when each medicine was first funded, brand changes, price changes, special-authority restrictions added or removed. This is unusual longitudinal data — most pharmaceutical regulators don't publish full historical schedules.
- **Special Authority**: many medicines have access restrictions (only funded for specific conditions, after first-line failure, etc.). The `special_authority` field flags these.
- **Subsidy ≠ price**: PHARMAC subsidises medicines; patients sometimes still pay a co-payment ($5 standard for funded scripts). Multi-source brands may have different patient prices despite identical funding.
- **Funding decisions are precedent-setting**: when PHARMAC funds a new medicine, that decision is sometimes the model overseas regulators reference. Tracking historical funding decisions has international value.
- **Section 29 medicines**: prescribed but unfunded — patients pay full retail. Not in the funded schedule; check pharmacy retail databases instead.

---

## Where to find more

- **PHARMAC datasets on eolas**: [eolas.fyi/datasets?source=PHARMAC](https://eolas.fyi/datasets?source=PHARMAC)
- **PHARMAC portal**: [pharmac.govt.nz](https://pharmac.govt.nz)
- **Current Schedule** (consumer view): [schedule.pharmac.govt.nz](https://schedule.pharmac.govt.nz)
- **Funding decisions + consultations**: [pharmac.govt.nz/medicines/decisions-and-consultations](https://pharmac.govt.nz/medicines/decisions-and-consultations)

## Related

- [Stats NZ source guide](statsnz.md) — for population denominators
- [ACC source guide](acc.md) — for ACC-funded diagnostic imaging + elective surgery data
- [Examples](../examples/index.md) — worked code recipes
