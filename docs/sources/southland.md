# Southland Councils data via eolas

The Southland region covers ~105,000 people across [Environment Southland](https://www.es.govt.nz) (ES) and three territorial authorities — Gore, Invercargill, and Southland District (which alone covers ~32,000 km² — the largest TA in NZ by area). eolas serves **48 datasets** — heavy on the freshwater + farming side, reflecting Southland's intensive dairying + sheep/beef economy.

If you're doing Southland property research, water-quality / catchment work, or agricultural-land analysis — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| Southland District (SDC) | sdc | 20 | Largest area + most layers — DP zones, designations, hazards, infrastructure |
| Invercargill City (ICC) | icc | 11 | City DP zones + hazards + heritage |
| Environment Southland (ES) | es | 10 | Catchment degradation (E. coli, nitrogen), liquefaction, physiographic zones, land use 2025 |
| Gore District | gore | 7 | DP designations + hazards |

### Standout datasets

- `es_southland_land_use_2025` — current Southland land-use map (one of few council-current land-use rasters in NZ)
- `es_catchment_degradation_ecoli`, `es_catchment_degradation_total_n` — water-quality status by catchment (relevant for farm-environment-plan compliance)
- `es_physiographic_zones` — soil + climate composite that drives nutrient leaching modelling
- `es_significant_wetlands` — protected wetland areas
- `es_tsunami_evacuation_zones` — Southland coastal exposure (Foveaux Strait)
- `gore_earthquake_priority_buildings` — earthquake-prone building register

Browse: [eolas.fyi/datasets?source=Southland+Councils](https://eolas.fyi/datasets?source=Southland%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. ES publishes via [es.govt.nz/data](https://www.es.govt.nz/data); SDC + ICC via ArcGIS portals.

---

## License

All Southland council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

---

## Common patterns

### Catchment water-quality lookup

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(168.3478, -46.4131)], crs="EPSG:4326")  # central Invercargill
ecoli = client.southland("es_catchment_degradation_ecoli", as_sf=True)
hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), ecoli, predicate="within")
if len(hit):
    print(f"Catchment E. coli status: {hit['degradation_class'].iloc[0]}")
```

### Land-use composition

```python
lu = client.southland("es_southland_land_use_2025", as_sf=True)
lu["area_ha"] = lu.to_crs("EPSG:2193").area / 10_000
by_class = lu.groupby("land_use_class")["area_ha"].sum().sort_values(ascending=False)
print(by_class.head(15))
```

### Earthquake-prone buildings (Gore)

```python
epb = client.southland("gore_earthquake_priority_buildings", as_sf=True)
print(epb.groupby("status").size())  # remediated, partial, outstanding
```

---

## Source-specific notes

- **ES land-use map is unusually current**: 2025 vintage. Most regional councils don't publish recent land-use rasters — Southland + Otago do.
- **Physiographic zones drive nutrient policy**: `es_physiographic_zones` is the basis for Southland's nutrient-allocation methodology. Used in farm-environment plan + consent-renewal contexts.
- **Tsunami exposure**: while not as exposed as the BoP / East Coast, Southland still has tsunami evacuation zones for the Foveaux Strait + Bluff Peninsula.
- **Southland District size**: SDC covers 32,000 km² — second only to Auckland Council by area (and the largest by land area on the South Island). Its district plan is correspondingly large.
- **Contaminated sites**: Gore + Invercargill publish contaminated-land registers — relevant for industrial / brownfield property research.

---

## Where to find more

- **Southland datasets on eolas**: [eolas.fyi/datasets?source=Southland+Councils](https://eolas.fyi/datasets?source=Southland%20Councils)
- **ES data**: [www.es.govt.nz/data](https://www.es.govt.nz/data)
- **SDC**: [data.southlanddc.govt.nz](https://data.southlanddc.govt.nz)

## Related

- [Councils overview](councils.md) | [Examples](../examples/index.md)
