# Co-Lab Waikato data via eolas

[Co-Lab](https://www.co-lab.co.nz) is a 10-council shared-services consortium in the Waikato region — Hamilton City + Hauraki, Matamata-Piako, Ōtorohanga, Rotorua-Lakes, South Waikato, Taupō, Waikato, Waipa, and Waitomo district councils. eolas serves **79 datasets** from this consortium, all via a single shared Koordinates portal. This is the largest single-portal council cluster in eolas.

If you're doing Waikato-region planning, hazard, or rural-development work — this is the source. Hamilton City + Taupō + Matamata-Piako (Putāruru / Tirau) dominate by dataset count.

---

## What's in the catalogue

The Co-Lab portal serves each council's own datasets but normalises publishing format. Coverage by council:

| Council | Code | Datasets | Notes |
|---|---|---|---|
| Thames-Coromandel District | tcdc | 28 | Most comprehensive — full DP suite + hazards + coastal |
| Matamata-Piako District | mpdc | 12 | DP zones, designations, hazards |
| Taupō District | tpdc | 11 | DP zones + geothermal protection + Tongariro overlay |
| Waikato District | wdc | 8 | DP zones, designations |
| Waipa District | wpa | 4 | Basic DP coverage |
| Ōtorohanga | odc | 2 | Designated areas |
| Rotorua Lakes | rlc | 2 | Council layers (separate from BoPRC's regional data) |
| South Waikato | swdc | 2 | Basic |
| Hamilton City | hcc | 1 | District plan zoning |
| Hauraki | hdc | 1 | Reserve boundaries |

Waikato Regional Council (WRC) — 8 datasets — covers regional environmental + hazard layers.

Browse the full list: [eolas.fyi/datasets?source=Co-Lab+Waikato](https://eolas.fyi/datasets?source=Co-Lab%20Waikato).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. The Co-Lab portal updates as each council publishes — typically monthly+ cadence. WRC publishes via its own portal but the schedule is similar.

```python
meta = client.info("tcdc_district_plan_zones")
meta["last_refreshed_at"]
```

---

## License

All Co-Lab + WRC data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; per-council attribution required.

Recommended attribution: *"Source: [Council name] via Co-Lab Waikato, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Cross-council DP zone comparison

Co-Lab's strength is that all 10 councils use a normalised publishing schema, so you can cross-compare without per-council schema munging:

```python
councils = ["tcdc", "mpdc", "tpdc", "wdc", "wpa"]
zones = {}
for code in councils:
    try:
        z = client.colab_waikato(f"{code}_district_plan_zones", as_sf=True)
        zones[code] = z["zone_name"].value_counts().head(5)
    except Exception:
        pass

import pandas as pd
print(pd.DataFrame(zones).fillna(0).astype(int))
```

### Thames-Coromandel coastal exposure

```python
import geopandas as gpd
tcdc_coastal = client.colab_waikato("tcdc_coastal_inundation", as_sf=True)
tcdc_erosion = client.colab_waikato("tcdc_coastal_erosion", as_sf=True)
# Combined coastal-risk footprint
combined_area_km2 = pd.concat([tcdc_coastal, tcdc_erosion]).to_crs("EPSG:2193").area.sum() / 1e6
print(f"Coastal-risk area in Thames-Coromandel: {combined_area_km2:.0f} km²")
```

---

## Source-specific notes

- **Consortium = shared portal, not shared data ownership**: each council retains ownership of its data; Co-Lab just runs the publishing pipeline. Attribution is per-council.
- **TCDC dominates by count**: Thames-Coromandel publishes more layers than the others — full DP2025 area-overlay suite, hazards, coastal. Other councils publish a more minimal core.
- **WRC is published separately**: Waikato Regional Council uses its own portal — most regional-scale layers (river flows, water allocation, biodiversity) live there. Look for `wrc_*` prefixed datasets within this cluster.
- **Hamilton City has only 1 dataset (so far)**: that's not because HCC has no open data — they publish via their own [data.hamilton.govt.nz](https://data.hamilton.govt.nz). Only the DP zoning currently crosswalks into Co-Lab. Expanding HCC coverage is on the eolas roadmap.
- **Rotorua Lakes appears in two clusters**: most Rotorua datasets are in [Bay of Plenty Councils](bay-of-plenty.md) (because it's on BoPRC's portal), but the council also publishes via Co-Lab. Not duplicates — different data, different portals.
- **Taupō geothermal protection**: `tpdc_*_geothermal` layers (where present) regulate the geothermal resource — important for tourism / energy / consenting analysis.

---

## Where to find more

- **Co-Lab Waikato datasets on eolas**: [eolas.fyi/datasets?source=Co-Lab+Waikato](https://eolas.fyi/datasets?source=Co-Lab%20Waikato)
- **Co-Lab Waikato Open Data**: [data-waikatocouncils.opendata.arcgis.com](https://data-waikatocouncils.opendata.arcgis.com)
- **WRC**: [www.waikatoregion.govt.nz](https://www.waikatoregion.govt.nz)
- **Hamilton City separately**: [data.hamilton.govt.nz](https://data.hamilton.govt.nz)

## Related

- [Councils overview](councils.md)
- [Examples](../examples/index.md)
