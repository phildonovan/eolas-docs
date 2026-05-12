# Bay of Plenty Councils data via eolas

The Bay of Plenty region covers ~350,000 people across [Bay of Plenty Regional Council](https://www.boprc.govt.nz) (BoPRC, "Toi Moana") and five territorial authorities — Kawerau, Ōpōtiki, Rotorua-Lakes, Tauranga, and Western Bay of Plenty. eolas serves **46 datasets** spanning the region — with particularly strong tsunami + volcanic hazard data reflecting Bay of Plenty's geophysical setting.

If you're doing Bay of Plenty planning, hazard, or coastal-management work — this is the source.

---

## What's in the catalogue

### BoPRC — 10 datasets

| Theme | Datasets |
|---|---|
| **Tsunami** | `boprc_tsunami_evacuation_2025`, `boprc_tsunami_inundation_2500yr` |
| **Hazards** | `boprc_historic_flood_extents`, `boprc_liquefaction_level_b` |
| **Regional Coastal Environment Plan (RCEP)** | `boprc_rcep_ascv` (areas of significant cultural value), `boprc_rcep_coastal_environment_zone`, `boprc_rcep_historic_heritage_coastal`, `boprc_rcep_ibda_a`, `boprc_rcep_ibda_b`, `boprc_rcep_onfl` (outstanding natural features + landscapes) |

### Tauranga City Council (TCC) — 14 datasets

The region's largest urban centre + the country's busiest port. Coverage spans district plan zones, designations, hazards (coastal, flood, liquefaction), heritage, and infrastructure.

### Western Bay of Plenty (WBOPDC) — 8 datasets

District plan zones + hazards covering the urban-rural fringe around Tauranga.

### Rotorua-Lakes (WKDC pattern, 6 datasets), Ōpōtiki (5), Kawerau (3)

Smaller TAs — district plan zones, heritage sites, basic hazard layers.

Browse the full list at [eolas.fyi/datasets?source=Bay+of+Plenty+Councils](https://eolas.fyi/datasets?source=Bay%20of%20Plenty%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Most BoP councils publish via ArcGIS portals; BoPRC uses [data.boprc.govt.nz](https://data.boprc.govt.nz).

```python
meta = client.info("boprc_tsunami_evacuation_2025")
meta["last_refreshed_at"]
```

---

## License

All BoP council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; per-council attribution required.

Recommended attribution: *"Source: [Council name], served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Tsunami evacuation zone lookup (BoPRC scenario)

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(176.1651, -37.6878)], crs="EPSG:4326")  # central Tauranga
evac = client.bay_of_plenty("boprc_tsunami_evacuation_2025", as_sf=True)
zone = gpd.sjoin(pt.to_frame("g").set_geometry("g"), evac, predicate="within")
print("Tsunami evacuation zone:", zone["zone_name"].iloc[0] if len(zone) else "none")
```

### Coastal protection overlay

```python
coastal = client.bay_of_plenty("boprc_rcep_coastal_environment_zone", as_sf=True)
historic = client.bay_of_plenty("boprc_rcep_historic_heritage_coastal", as_sf=True)
# Combined coastal protection footprint
import pandas as pd
combined = pd.concat([coastal, historic])
print(f"Coastal protection area: {combined.to_crs('EPSG:2193').area.sum() / 1e6:.0f} km²")
```

---

## Source-specific notes

- **BoP has high geophysical hazard**: White Island / Whakaari, Mt Tarawera, Rotorua geothermal systems, Hikurangi subduction interface — tsunami + volcanic + earthquake hazards are real and well-modelled.
- **Tauranga has separate publishing**: TCC's data is on its own portal; some layers overlap with BoPRC's regional layers. For property-level planning, use TCC's; for regional-scale risk, use BoPRC's.
- **Ōpōtiki tsunami**: `opotiki_coastal_hazard_ohiwa` covers the Ōhiwa Harbour — particularly exposed to tsunami; check before coastal investment decisions.
- **RCEP coverage**: the BoP Regional Coastal Environment Plan layers are statutory + binding on coastal subdivision / development. Use these (not BoPRC's general planning data) when assessing coastal-zone constraints.
- **Rotorua geothermal**: the geothermal field underlying Rotorua city has specific consenting rules (sourced via Rotorua Lakes Council); not all geothermal-protection layers are yet in eolas.

---

## Where to find more

- **BoP datasets on eolas**: [eolas.fyi/datasets?source=Bay+of+Plenty+Councils](https://eolas.fyi/datasets?source=Bay%20of%20Plenty%20Councils)
- **BoPRC data portal**: [data.boprc.govt.nz](https://data.boprc.govt.nz)
- **Tauranga GIS**: [data.tauranga.govt.nz](https://data.tauranga.govt.nz)

## Related

- [Councils overview](councils.md)
- [LINZ](linz.md) — cadastral parcels
- [Examples](../examples/index.md)
