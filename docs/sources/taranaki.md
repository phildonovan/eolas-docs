# Taranaki Councils data via eolas

The Taranaki region covers ~130,000 people across [Taranaki Regional Council](https://www.trc.govt.nz) (TRC) and three territorial authorities — New Plymouth, South Taranaki, and Stratford. eolas serves **33 datasets** — with Taranaki's defining feature, Mount Taranaki / Egmont, driving significant volcanic-hazard mapping.

If you're doing Taranaki property research, volcanic-hazard work, or coastal-region planning — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| New Plymouth District (NPDC) | npdc | 17 | Most comprehensive DP suite + coastal hazards + volcanic hazard + heritage |
| TRC | trc | 12 | Regional planning + freshwater + coastal management |
| South Taranaki District (STDC) | stdc | 4 | Basic DP coverage |

### Standout datasets

- `npdc_dp_operative_volcanic_hazard` — Mount Taranaki volcanic-hazard zones in NPDC's operative district plan
- `npdc_dp_operative_fault_hazard` — fault-avoidance zones (Cape Egmont fault)
- `npdc_dp_operative_coastal_erosion`, `npdc_dp_operative_coastal_flooding` — coastal hazards (NPDC's coastline is exposed)
- `npdc_dp_operative_devarea` — development areas in NPDC's plan
- `trc_*_freshwater_*` — water-allocation + freshwater management areas across the ring plain

Browse: [eolas.fyi/datasets?source=Taranaki+Councils](https://eolas.fyi/datasets?source=Taranaki%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. NPDC + TRC publish via ArcGIS portals.

---

## License

All Taranaki council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

---

## Common patterns

### Volcanic-hazard exposure (Mt Taranaki)

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(174.0760, -39.0586)], crs="EPSG:4326")  # central New Plymouth
volcanic = client.taranaki("npdc_dp_operative_volcanic_hazard", as_sf=True)
hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), volcanic, predicate="within")
print(f"In volcanic-hazard zone: {'YES' if len(hit) else 'no'}")
if len(hit):
    print(f"  Zone: {hit['hazard_zone'].iloc[0]}")
```

### Combined hazard footprint (volcanic + fault + coastal)

```python
import geopandas as gpd
import pandas as pd

layers = [
    "npdc_dp_operative_volcanic_hazard",
    "npdc_dp_operative_fault_hazard",
    "npdc_dp_operative_coastal_erosion",
    "npdc_dp_operative_coastal_flooding",
]
all_hazards = pd.concat([client.taranaki(n, as_sf=True) for n in layers])
print(f"Combined hazard area: {all_hazards.to_crs('EPSG:2193').area.sum() / 1e6:.0f} km²")
```

---

## Source-specific notes

- **Mt Taranaki is the defining hazard**: it's a young, potentially-active stratovolcano. NPDC's volcanic-hazard layers reflect both ash/lahar pathways + lava-flow modelling. Used in consenting for new residential builds in zoned areas.
- **Ring plain dairy + freshwater**: TRC's freshwater management overlays are critical for dairy + horticulture consents. The Taranaki ring plain has intensive land use and active water-allocation politics.
- **Coastal exposure**: Cape Egmont juts into prevailing south-westerly swells — coastal erosion is real and ongoing. NPDC publishes both *operative* (currently legal) + *proposed* (in consultation) coastal-hazard layers.
- **South Taranaki + Stratford**: limited current coverage. Both councils publish more via their own portals — on the eolas roadmap to expand.
- **Iwi context**: Taranaki iwi data (sites of significance) is being progressively added — check the live catalogue for current status.

---

## Where to find more

- **Taranaki datasets on eolas**: [eolas.fyi/datasets?source=Taranaki+Councils](https://eolas.fyi/datasets?source=Taranaki%20Councils)
- **TRC**: [www.trc.govt.nz](https://www.trc.govt.nz)
- **NPDC**: [data.npdc.govt.nz](https://data.npdc.govt.nz)

## Related

- [Councils overview](councils.md) | [Examples](../examples/index.md)
