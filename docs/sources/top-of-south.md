# Gisborne / Top of South Councils data via eolas

This cluster covers four geographically-dispersed unitary + city councils that don't sit neatly within a single regional-council area: Gisborne (East Coast), Marlborough, Nelson City, and Tasman District (top of the South Island). eolas serves **45 datasets** across the cluster.

Each of these is a *unitary authority* (regional + territorial functions combined) — so the data spans planning, hazards, and environmental management in one source.

If you're doing East-Coast cyclone-resilience research, Marlborough wine-country property analysis, or Nelson / Tasman coastal-region planning — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| Nelson City | nelson | 17 | DP zones, hazards, heritage — densest urban coverage in the cluster |
| Gisborne District (GDC) | gdc | 11 | Post-Gabrielle hazard suite, coastal management, wāhi tapu |
| Marlborough District (MDC) | mdc | 11 | Aquaculture management, coastal natural character, flood, designations |
| Tasman District | tasman | 6 | DP basics + coastal |

### Standout datasets

- `mdc_marl_aquaculture_mgmt_areas` — Marlborough Sounds aquaculture (mussel + salmon) management zones
- `gdc_coastal_*` — Gisborne's coastal hazard suite (post-Cyclone Gabrielle relevance)
- `gdc_waahi_tapu` — iwi-consented sacred site polygons
- `nelson_*_hazard` — Nelson's earthquake / liquefaction / flood layers
- `mdc_marl_coastal_natural_character_outstanding` — outstanding coastal character (Sounds-specific)

Browse: [eolas.fyi/datasets?source=Gisborne+%2F+Top+of+South+Councils](https://eolas.fyi/datasets?source=Gisborne%20%2F%20Top%20of%20South%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Each council publishes via its own ArcGIS / Koordinates portal.

---

## License

All cluster data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Per-council attribution required.

---

## Common patterns

### Marlborough Sounds aquaculture lookup

```python
aqua = client.top_of_south("mdc_marl_aquaculture_mgmt_areas", as_sf=True)
print(aqua["mgmt_class"].value_counts())  # mussel / salmon / mixed
```

### Gisborne post-Gabrielle coastal exposure

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(178.0099, -38.6623)], crs="EPSG:4326")  # central Gisborne
erosion = client.top_of_south("gdc_coastal_erosion", as_sf=True)
hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), erosion, predicate="within")
print(f"Gisborne coastal erosion zone: {'YES' if len(hit) else 'no'}")
```

---

## Source-specific notes

- **Four distinct economies**: this cluster groups councils by data-portal pattern (each is a unitary publishing its full suite), not by economic similarity. Gisborne's primary sector economy is very different from Nelson's seafood + tourism, Marlborough's wine + aquaculture, and Tasman's horticulture.
- **Marlborough aquaculture**: NZ's salmon + mussel industries are concentrated here. The aquaculture-management-area layers are statutory + binding on new farms.
- **Gisborne post-Gabrielle**: Cyclone Gabrielle (Feb 2023) caused major damage in Gisborne / Wairoa. Some post-event remapping is published; updates are ongoing.
- **Nelson + Tasman cross-boundary**: Nelson City + Tasman District share boundaries + some infrastructure. Always check both councils when doing the Nelson-Tasman urban area.
- **Wāhi tapu publishing**: GDC's wāhi tapu layer follows iwi-consented publication conventions; some sites are deliberately broad polygons to protect specific locations.

---

## Where to find more

- **Cluster datasets on eolas**: [eolas.fyi/datasets?source=Gisborne+%2F+Top+of+South+Councils](https://eolas.fyi/datasets?source=Gisborne%20%2F%20Top%20of%20South%20Councils)
- **Nelson**: [data.nelson.govt.nz](https://data.nelson.govt.nz)
- **MDC**: [arcgis.marlborough.govt.nz](https://arcgis.marlborough.govt.nz)
- **GDC**: [www.gdc.govt.nz](https://www.gdc.govt.nz)
- **Tasman**: [www.tasman.govt.nz](https://www.tasman.govt.nz)

## Related

- [Councils overview](councils.md) | [Examples](../examples/index.md)
