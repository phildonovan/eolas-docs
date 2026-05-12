# Manawatū-Whanganui Councils data via eolas

The Manawatū-Whanganui region covers ~260,000 people across [Horizons Regional Council](https://www.horizons.govt.nz) and seven territorial authorities — Horowhenua, Manawatū, Palmerston North, Rangitīkei, Ruapehu, Tararua, and Whanganui. eolas serves **46 datasets** with broad coverage of river-flood hazards (Manawatū River + tributaries), cultural sites, and the Ruapehu volcanic context.

If you're doing central-North-Island planning, agricultural / horticultural research, or volcanic + flood-hazard work — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| Horowhenua District (HoroW) | horow | 11 | DP zones, coastal/flood hazards, landscape, ONFL |
| Rangitīkei District | rdc | 10 | DP layers + Rangitīkei river flood + heritage |
| Horizons RC | horizons | 8 | Airsheds, groundwater/water mgmt areas, sites of cultural significance, SOS aquatic+riparian |
| Tararua District | tararua | 8 | District plan zones + heritage + hazards |
| Palmerston North City Council (PNCC) | pncc | 6 | City DP zones + flood + earthquake-prone buildings |
| Manawatū District (MDC, central) | mdc | 3 | Limited (basic DP layers) |

### Standout datasets

- `horizons_airshed_taihape`, `horizons_airshed_taumarunui` — modelled airsheds for inland centres (relevant for industrial / domestic-fire consenting)
- `horizons_groundwater_mgmt_area` — Manawatū basin groundwater zones (irrigation + drinking water context)
- `horizons_floodways_flood_prone_land` — regional flood hazard envelope
- `horizons_sites_significance_cultural` — iwi-consented site polygons
- `horow_dp_coastal_hazard` — Horowhenua's coast (Levin–Foxton–Hokio Beach line)

Browse the full list: [eolas.fyi/datasets?source=Manawat%C5%AB-Whanganui+Councils](https://eolas.fyi/datasets?source=Manawat%C5%AB-Whanganui%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Horizons publishes via its own ArcGIS portal; TAs use a mix of ArcGIS + Koordinates portals.

```python
meta = client.info("horizons_groundwater_mgmt_area")
meta["last_refreshed_at"]
```

---

## License

All Manawatū-Whanganui council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use fine; per-council attribution required.

---

## Common patterns

### River-flood exposure for a property

```python
import geopandas as gpd
from shapely.geometry import Point

pt = gpd.GeoSeries([Point(175.6113, -40.3523)], crs="EPSG:4326")  # central Palmerston North
floodways = client.manawatu_whanganui("horizons_floodways_flood_prone_land", as_sf=True)
hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), floodways, predicate="within")
print(f"In flood-prone land: {'YES' if len(hit) else 'no'}")
```

### Groundwater management context

```python
gw = client.manawatu_whanganui("horizons_groundwater_mgmt_area", as_sf=True)
print(gw.groupby("mgmt_unit").size())  # zones by management category
```

---

## Source-specific notes

- **Ruapehu District includes Mt Ruapehu**: active volcano + ski areas — volcanic-hazard layers from GeoNet (separate source) + DOC conservation land overlay are relevant for tourism / consenting in this area.
- **Manawatū River flood history**: the 2004 + 2015 floods drive much of the current flood mapping. `horizons_floodways_flood_prone_land` is the regulatory hazard layer; for historic events use council records.
- **Whanganui District is split**: most Whanganui council data lives in the [Napier + Whanganui cluster](napier-whanganui.md) (because both publish via the WhanganuiData portal), not this cluster.
- **Iwi cultural sites**: `horizons_sites_significance_cultural` has iwi-agreed publication boundaries. Treat as authoritative for the geometry but check the source metadata for any access restrictions.

---

## Where to find more

- **Manawatū-Whanganui datasets on eolas**: [eolas.fyi/datasets?source=Manawat%C5%AB-Whanganui+Councils](https://eolas.fyi/datasets?source=Manawat%C5%AB-Whanganui%20Councils)
- **Horizons RC data**: [www.horizons.govt.nz/about-us/maps-and-data](https://www.horizons.govt.nz/about-us/maps-and-data)
- **PNCC**: [data.pncc.govt.nz](https://data.pncc.govt.nz)

## Related

- [Councils overview](councils.md)
- [Napier + Whanganui guide](napier-whanganui.md) — for Whanganui city-council layers
- [Examples](../examples/index.md)
