# Northland Councils data via eolas

The Northland region covers ~200,000 people across [Northland Regional Council](https://www.nrc.govt.nz) (NRC, Taitokerau) and three territorial authorities — Far North, Kaipara, and Whangārei. eolas serves **28 datasets** with strong emphasis on coastal hazards (cyclone exposure) and biodiversity.

If you're doing Northland property research, cyclone-resilience planning, or biodiversity / pest-management analysis — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| NRC | nrc | 9 | Biodiversity ranking, coastal erosion + flood hazards, regional environment |
| Far North District (FNDC) | fndc | 7 | DP zones, designations, heritage, notable trees, outstanding landscapes, sites of significance to iwi/hapū |
| Whangārei District (WDC) | wdc | 7 | Council-managed asset + planning layers |
| Kaipara District (KDC) | kdc | 5 | Designations, flood hazards, geotechnical risk, heritage |

### Standout datasets

- `nrc_biodiversity_ranking` — NRC's regional biodiversity priority ranking
- `nrc_coastal_erosion_current` — current coastal-erosion zones (relevant for cyclone resilience post-Gabrielle)
- `nrc_coastal_flood_hazard_zones` — coastal flooding for storm-surge planning
- `fndc_sites_significance_maori` — iwi-consented site locations
- `kdc_geotechnical_hazard_risk` — landslide / slope-instability hazards (relevant for hill-country dairy farms)

Browse the full list: [eolas.fyi/datasets?source=Northland+Councils](https://eolas.fyi/datasets?source=Northland%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. NRC publishes via [arcgis.com/home (NRC org)](https://nrcgis.maps.arcgis.com); each TA via its own portal.

```python
meta = client.info("nrc_biodiversity_ranking")
meta["last_refreshed_at"]
```

---

## License

All Northland council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use fine; per-council attribution required.

---

## Common patterns

### Coastal-erosion exposure (post-Gabrielle relevance)

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(174.3187, -35.7275)], crs="EPSG:4326")  # central Whangārei
erosion = client.northland("nrc_coastal_erosion_current", as_sf=True)
flood = client.northland("nrc_coastal_flood_hazard_zones", as_sf=True)

erosion_hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), erosion, predicate="within")
flood_hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), flood, predicate="within")
print(f"Coastal erosion zone: {'YES' if len(erosion_hit) else 'no'}")
print(f"Coastal flood zone:   {'YES' if len(flood_hit) else 'no'}")
```

### Biodiversity hotspots

```python
bio = client.northland("nrc_biodiversity_ranking", as_sf=True)
# Top-priority sites (rank 1 = highest)
top = bio[bio["priority_rank"] == 1]
print(f"Highest-priority biodiversity sites: {len(top)}")
```

---

## Source-specific notes

- **Cyclone Gabrielle context**: Northland was severely impacted by Cyclone Gabrielle (Feb 2023). Coastal + flood hazard layers reflect pre-Gabrielle modelling; post-event remapping is in progress but not yet fully published.
- **Geotechnical risk in Kaipara**: hill-country landslide hazards drive insurance + consenting decisions — `kdc_geotechnical_hazard_risk` is the canonical source.
- **Mana whenua sites**: `fndc_sites_significance_maori` follows iwi-consented publication conventions. Some sensitive sites are deliberately broad polygons rather than exact points.
- **Far North + Whangārei coverage**: growing — each council publishes more layers on its own portal; integration into the eolas pipeline is rolling.

---

## Where to find more

- **Northland datasets on eolas**: [eolas.fyi/datasets?source=Northland+Councils](https://eolas.fyi/datasets?source=Northland%20Councils)
- **NRC GIS portal**: [nrcgis.maps.arcgis.com](https://nrcgis.maps.arcgis.com)
- **FNDC**: [www.fndc.govt.nz](https://www.fndc.govt.nz)
- **WDC**: [www.wdc.govt.nz](https://www.wdc.govt.nz)
- **KDC**: [www.kaipara.govt.nz](https://www.kaipara.govt.nz)

## Related

- [Councils overview](councils.md) | [Examples](../examples/index.md)
