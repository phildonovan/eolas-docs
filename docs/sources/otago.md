# Otago Councils data via eolas

The Otago region covers ~250,000 people across [Otago Regional Council](https://www.orc.govt.nz) (ORC) and five territorial authorities — Central Otago, Clutha, Dunedin, Queenstown-Lakes, and Waitaki. eolas serves **41 datasets** — with heavy weighting toward Queenstown-Lakes (tourism + hazards) and ORC (water + land use).

If you're doing Otago property research, alpine-tourism planning, or water-allocation analysis — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| Queenstown-Lakes (QLDC) | qldc | 22 | District Plan + ski-area overlays + landscape protection + Queenstown airport noise |
| Otago Regional Council (ORC) | orc | 9 | Land use 2024, irrigated areas, groundwater protection, flood (incl. Roxburgh debris) |
| Dunedin City Council (DCC) | dcc | 7 | 2nd Generation District Plan (2GP) zones, designations, heritage, significant trees |
| Waitaki District (WDC) | wdc | 2 | District plan basics |
| Clutha District | clutha | 1 | Resource areas |

### Standout datasets

| Dataset | Description |
|---|---|
| `orc_otago_land_use_2024` | ORC's 2024 land-use map for the region — one of the few council-published current land-use rasters in NZ. |
| `orc_otago_irrigated_areas` | Modelled irrigated farmland — useful for dairying / pastoral analysis. |
| `orc_roxburgh_debris_flood_max_credible` | Maximum credible debris-flood scenario for Roxburgh — distinct from standard return-period mapping. |
| `dcc_2gp_zones` | Dunedin's "2nd Generation District Plan" — the operative plan post-2019. |
| `qldc_*` (suite) | Comprehensive Queenstown-Lakes coverage — alpine + lakeside + airport overlays. |

Browse the full list: [eolas.fyi/datasets?source=Otago+Councils](https://eolas.fyi/datasets?source=Otago%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. ORC publishes via [data.orc.govt.nz](https://data.orc.govt.nz); QLDC via its own ArcGIS portal; DCC via [opendata.dunedin.govt.nz](https://opendata.dunedin.govt.nz).

```python
meta = client.info("orc_otago_land_use_2024")
meta["last_refreshed_at"]
```

---

## License

All Otago council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use fine; per-council attribution required.

---

## Common patterns

### Queenstown-Lakes property due diligence

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(168.6626, -45.0312)], crs="EPSG:4326")  # central Queenstown

# Common QLDC layers worth checking
layers = [
    "qldc_district_plan_zones",
    "qldc_outstanding_natural_landscapes",
    "qldc_visual_amenity_landscapes",
    "qldc_natural_hazards",
]
for name in layers:
    try:
        layer = client.otago(name, as_sf=True)
        hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), layer, predicate="within")
        print(f"  {name}: {'YES' if len(hit) else 'no'}")
    except Exception as e:
        print(f"  {name}: skipped ({e})")
```

### Land-use composition (ORC 2024)

```python
import geopandas as gpd

lu = client.otago("orc_otago_land_use_2024", as_sf=True)
lu["area_ha"] = lu.to_crs("EPSG:2193").area / 10_000
by_class = lu.groupby("land_use_class")["area_ha"].sum().sort_values(ascending=False)
print(by_class.head(15))
```

---

## Source-specific notes

- **QLDC publishes more than the count suggests**: the 22 layers in eolas are a subset of QLDC's public portal — additional cycle network + parks + heritage layers are on the roadmap.
- **ORC's land-use map is unusually current**: most regional councils don't publish a recent land-use raster. ORC's 2024 layer is genuinely current and high-value for primary-sector analytics.
- **Roxburgh debris-flow data**: Otago has specific historical landslide / debris-flow hazards around Roxburgh; the max-credible layer reflects worst-case scenarios used in consenting.
- **Dunedin's 2GP**: the second-generation district plan replaced Dunedin's 1st-generation plan in 2019. `dcc_2gp_*` layers are the current operative; older `dcc_*` (where they exist) are deprecated.
- **Queenstown airport overlays**: critical for residential development in the basin — `qldc_airport_*` layers (where present) capture noise + obstacle limit surfaces.
- **Central Otago, Clutha, Waitaki**: limited current coverage. Their districts have less data on shared portals; on the roadmap to expand.

---

## Where to find more

- **Otago datasets on eolas**: [eolas.fyi/datasets?source=Otago+Councils](https://eolas.fyi/datasets?source=Otago%20Councils)
- **ORC data**: [data.orc.govt.nz](https://data.orc.govt.nz)
- **QLDC GIS**: [gis.qldc.govt.nz](https://gis.qldc.govt.nz)
- **DCC**: [opendata.dunedin.govt.nz](https://opendata.dunedin.govt.nz)

## Related

- [Councils overview](councils.md)
- [Examples](../examples/index.md)
