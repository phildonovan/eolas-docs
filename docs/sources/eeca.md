# EECA data via eolas

The [Energy Efficiency and Conservation Authority](https://www.eeca.govt.nz) (EECA) runs New Zealand's energy-efficiency programmes — funding EV charging infrastructure, modelling industrial heat demand, and publishing the Energy End-Use Database (EEUD). eolas serves **6 datasets** from EECA — covering the data the EV and decarbonisation policy worlds depend on.

If you're doing energy-transition modelling, EV-infrastructure planning, or industrial-decarbonisation research — EECA is the source.

---

## What's in the catalogue

### EV charging

| Dataset | Description |
|---|---|
| `eeca_ev_chargers_public` | All publicly accessible EV charging units in NZ with location, owner, operator, plug type, power. |
| `eeca_ev_chargers_cofunded` | EV charging sites that received EECA co-funding support — applicant, status, funding. |
| `eeca_ev_metrics_region` | Summary EV adoption + charging infrastructure metrics by NZ region — registrations, charger counts. |
| `eeca_ev_metrics_district` | Same EV metrics by territorial authority. |

### Energy + industrial

| Dataset | Description |
|---|---|
| `eeca_energy_end_use` | EECA's Energy End Use Database (EEUD) — energy consumption by sector + end use, 2017+. |
| `eeca_regional_heat_demand` | Industrial heat demand + boiler capacity by region + sector, broken down by fuel + temperature band. |

---

## Refresh schedule

Quarterly. EECA publishes EEUD annually; EV charger + metrics quarterly; regional heat demand annually after EECA's industrial decarbonisation modelling cycle. Our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("eeca_ev_chargers_public")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All EECA data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: EECA (Energy Efficiency and Conservation Authority), served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### EV charging coverage by region

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    chargers = client.eeca("eeca_ev_chargers_public", as_sf=True)
    by_region = chargers.groupby("region").size().sort_values(ascending=False)
    by_region.head(10).plot.barh(title="Public EV chargers by region")
    plt.show()
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    chargers <- eolas_get_eeca("eeca_ev_chargers_public", as_sf = TRUE)
    by_region <- chargers |> count(region) |> arrange(desc(n))
    ggplot(head(by_region, 10), aes(reorder(region, n), n)) +
      geom_col() + coord_flip() +
      labs(title = "Public EV chargers by region")
    ```

### EV adoption + charging gap

```python
metrics = client.eeca("eeca_ev_metrics_district")
# Districts with EV registrations growing faster than charger rollout
metrics["ev_per_charger"] = metrics["ev_registrations"] / metrics["chargers_per_district"]
print(metrics.sort_values("ev_per_charger", ascending=False).head(15)[["district", "ev_per_charger"]])
```

### Industrial heat demand by sector

```python
heat = client.eeca("eeca_regional_heat_demand")
# By sector + temperature band (drives boiler-replacement priorities)
pivot = heat.pivot_table(values="heat_demand_gwh", index="sector", columns="temp_band", aggfunc="sum")
print(pivot)
```

### Energy end-use by sector

```python
eeud = client.eeca("eeca_energy_end_use")
# Latest year, by sector
latest = eeud[eeud["year"] == eeud["year"].max()]
print(latest.groupby("sector")["energy_pj"].sum().sort_values(ascending=False))
```

---

## Source-specific notes

- **EECA public chargers vs NZTA**: EECA's `eeca_ev_chargers_public` is similar to NZTA's `nzta_ev_charging` but published independently. EECA's data is more current for sites EECA co-funded; NZTA is broader. Use both for a complete picture.
- **EEUD methodology**: the Energy End Use Database is a *modelled* product — it combines census data, energy retail data, and end-use surveys to estimate consumption. Not measured at the meter; expect ±10-15% uncertainty on individual cells.
- **Heat demand temperature bands**: industrial heat is classified by required temperature (typically <100°C, 100-300°C, >300°C). Lower-temperature processes (food, drying) are more electrifiable than high-temperature ones (cement, steel).
- **Co-funding status**: charger sites that received EECA funding are flagged in `_cofunded`. Useful for policy evaluation (did co-funding fill the right gaps?).
- **District-level EV metrics**: a useful proxy for council-level decarbonisation reporting. EECA also publishes vehicle-fleet data not (yet) in eolas.
- **Charging "speed" tiers**: data distinguishes Level 1 (slow), Level 2 (medium), DC fast (50-150kW), DC ultra-fast (150+kW). Different infrastructure types serve different use cases (overnight at home vs road trip).

---

## Where to find more

- **EECA datasets on eolas**: [eolas.fyi/datasets?source=EECA](https://eolas.fyi/datasets?source=EECA)
- **EECA EV charging open data**: [www.eeca.govt.nz/insights/data-tools-and-resources/ev-charging-infrastructure-database](https://www.eeca.govt.nz/insights/data-tools-and-resources/ev-charging-infrastructure-database)
- **EECA EEUD**: [www.eeca.govt.nz/insights/data-tools-and-resources/energy-end-use-database](https://www.eeca.govt.nz/insights/data-tools-and-resources/energy-end-use-database)

## Related

- [NZTA source guide](nzta.md) — for the separate NZTA EV charging dataset
- [MBIE source guide](mbie.md) — for fuel + gas energy statistics
- [Examples](../examples/index.md) — worked code recipes
