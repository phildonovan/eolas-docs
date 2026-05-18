# Council data via eolas

New Zealand has 67 territorial authorities (TAs) — 11 city councils, 50 district councils, and 6 unitary authorities (which combine TA + regional council functions) — plus 11 regional councils on top. eolas aggregates ~600 datasets across **15 council clusters** spanning the entire country, normalising the patchwork of ArcGIS, Koordinates, and bespoke portals into a consistent schema.

Coverage is ~99% of NZ population — 64 of 67 TAs are included, plus all 11 regional councils. (Three small TAs don't publish open data; we don't fabricate it.)

If you're doing planning, hazard, or infrastructure analysis where district-plan boundaries, flood hazards, mana whenua sites, or municipal assets matter — this is where to look.

---

## How councils are clustered

We group councils into **15 regional clusters** for two reasons:

1. **Regional councils share data with their territorial authorities.** ECan publishes much of its work on the same Koordinates portal as Selwyn, Christchurch, Waimakariri, etc. — sharing a cluster means one pipeline.
2. **The clusters match how planners and infrastructure people actually work.** "Wellington data" includes GWRC + Hutt + Porirua + Wellington City + Kāpiti + Carterton + Masterton + South Wairarapa + Upper Hutt — all relevant to most Wellington-region questions.

| Cluster | Datasets | Population | Guide |
|---|---|---|---|
| [Auckland Council](auckland-council.md) | 20 | 1.7M | District Plan overlays |
| [Auckland Transport](auckland-transport.md) | 10 | 1.7M | Bus/ferry/train + cycle |
| [Wellington Region Councils](wellington.md) | 76 | 540k | GWRC + 8 TAs |
| [ECan / Canterbury](canterbury.md) | 85 | 670k | ECan + 7 TAs (incl. Christchurch) |
| [Co-Lab Waikato](colab-waikato.md) | 79 | 530k | 10-council consortium |
| [Bay of Plenty](bay-of-plenty.md) | 46 | 350k | BoPRC + 5 TAs |
| [Otago Councils](otago.md) | 41 | 250k | ORC + 5 TAs (incl. Queenstown) |
| [Manawatū-Whanganui](manawatu-whanganui.md) | 46 | 260k | Horizons + 7 TAs |
| [Gisborne / Top of South](top-of-south.md) | 45 | 270k | Gisborne, Marlborough, Nelson, Tasman |
| [Southland Councils](southland.md) | 48 | 105k | ES + Invercargill, Gore, Southland District |
| [Hawke's Bay Councils](hawkes-bay.md) | 33 | 180k | HBRC + Central Hawke's Bay (other TAs in separate clusters) |
| [Taranaki Councils](taranaki.md) | 33 | 130k | TRC + New Plymouth, South Taranaki, Stratford |
| [Northland Councils](northland.md) | 28 | 200k | NRC + Far North, Kaipara, Whangārei |
| [West Coast (Te Tai o Poutini)](west-coast.md) | 24 | 33k | WCRC + Buller, Grey, Westland (shared TTPP plan) |
| [Napier + Whanganui](napier-whanganui.md) | 20 | 75k + 50k | Napier City + Whanganui District (city-council layers) |

---

## What you'll find in council data

Most clusters share a similar palette of layers — what differs is the regional emphasis (e.g. earthquake hazards loom larger in Canterbury; cyclone exposure in Northland and Hawke's Bay).

### District plan layers

District plans are the legal planning framework for each TA. Most TAs publish:

- **Zones** — residential, business, rural, industrial, mixed-use, etc.
- **Designations** — sites reserved for specific purposes (schools, transmission corridors, hospitals).
- **Overlays** — heritage areas, coastal areas, natural features, hazards.
- **Precincts** — special-character or themed sub-areas.

These come from each council's operative + proposed district plan; eolas serves the current operative version by default, with proposed versions tagged where available.

### Hazards

A common set across most regions:

- **Flood hazards** — historic flood extents, modelled future scenarios (typically 50yr / 100yr / 200yr / 500yr return periods).
- **Earthquake** — fault avoidance zones, liquefaction risk, ground shaking amplification.
- **Coastal** — erosion zones, coastal flooding, sea-level-rise inundation.
- **Tsunami** — evacuation zones, modelled inundation (varies in return period from 100yr to 2500yr).
- **Volcanic** — Taranaki + Auckland clusters have specific volcanic-hazard layers.

### Cultural + heritage

- **Sites of significance to mana whenua / wāhi tapu** — confidential locations marked where iwi/hapū have agreed to publication; many councils suppress exact locations for protection.
- **Heritage areas + heritage buildings** — listed under the Resource Management Act and/or Historic Places Trust.
- **Archaeological sites** — usually as point or polygon overlays.

### Infrastructure + assets (varies)

- **Three Waters** (water, wastewater, stormwater) — published by some councils; many keep it internal.
- **Roads** — usually just centrelines or "council-owned" subset; the NZTA layer ([Waka Kotahi guide](nzta.md)) covers state highways.
- **Parks, reserves, council-owned buildings** — varies in detail.

### Environmental (regional councils only)

- **Coastal marine area** — RMA boundary.
- **Air sheds** — for monitoring + regulation.
- **Significant natural areas (SNAs)** — biodiversity hotspots.
- **Resource consents** — current discharges, takes, abstractions.

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Councils don't publish on a coordinated cadence — most update on their own irregular schedule when a plan change is notified, a hazard map is revised, or a new consent is issued. The weekly refresh catches whatever's changed at source.

```python
meta = client.info("akc_aircraft_noise_overlay")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

The vast majority of council open-data layers are **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. A few specific layers have local restrictions (typically Three Waters infrastructure and cultural sites). Always check the per-dataset metadata before commercial redistribution.

Recommended attribution: *"Source: [Council name], served via eolas (eolas.fyi). CC-BY 4.0."* — substitute the specific council, since each is the licence-holder for its own data.

For multi-council analysis (e.g. nationwide hazard maps), use a generic attribution: *"Source: NZ Councils via eolas (eolas.fyi). CC-BY 4.0 — see eolas dataset metadata for per-source attribution."*

---

## Common patterns

### Find every council's district-plan zones

```python
import pandas as pd

# Most clusters use a `*_district_plan_zones` or `*_dp_zones` naming pattern
datasets = client.list()
zones = [d["name"] for d in datasets if "district_plan_zones" in d["name"].lower() or "_dp_zones" in d["name"].lower()]
print(f"Found {len(zones)} district-plan zone datasets")
```

### Hazard exposure for a parcel

The workflow most consulting / planning use cases follow:

```python
import geopandas as gpd
from shapely.geometry import Point

# 1. Pick a location (lat, lon)
pt = gpd.GeoSeries([Point(174.7762, -41.2865)], crs="EPSG:4326")

# 2. Which TA contains this point?
ta = client.linz("nz_territorial_authority_2023", as_sf=True)
location_ta = gpd.sjoin(pt.to_frame("geom").set_geometry("geom"), ta, predicate="within")
ta_name = location_ta["ta_name"].iloc[0]

# 3. Load that TA's flood + earthquake hazards
# (dataset name varies; this is a Wellington example)
flood = client.wellington("gwrc_flood_hazard_extents", as_sf=True)
flood_at_point = gpd.sjoin(pt.to_frame("geom").set_geometry("geom"), flood, predicate="within")

print(f"Location: {ta_name}")
print(f"In flood-hazard area: {len(flood_at_point) > 0}")
```

A native "what's at this point" API is on the eolas roadmap. For now, the workflow is: fetch the relevant council layer + spatial-join in-memory.

### District-plan compatibility across regions

District plans share a common vocabulary (zones, designations, overlays) but each council names columns differently. The eolas pipeline standardises basic columns (`geometry_wkt`, `_eolas_*` metadata) but per-council attribute schemas are preserved. Use `client.info(name)` to inspect the schema before joining cross-region.

---

## Source-specific notes

- **Coverage gaps**: 3 TAs (Chatham Islands, Stewart Island, Mackenzie District) don't publish open data and aren't in eolas. The [council coverage memo](https://github.com/phildonovan/eolas/blob/main/docs/council-coverage.md) tracks exactly what's in and out.
- **District plan version**: most clusters serve the *operative* district plan. Where a *proposed* version exists, it's served as a separate dataset (suffixed `_proposed`).
- **Co-Lab Waikato is a consortium**: 10 councils share one Koordinates portal — that's why their cluster has 79 datasets despite covering "smaller" individual councils.
- **Wellington Region's 76 includes Carterton, Hutt, Kāpiti, Masterton, Porirua, South Wairarapa, Upper Hutt, Wellington City + the regional council**: it's effectively the entire Wellington administrative area.
- **Northland Councils' 28 includes Far North + Kaipara + Whangārei + NRC**: which covers the entire Northland region.
- **ECan / Canterbury's 85 includes Ashburton, Christchurch, Hurunui, Selwyn, Timaru, Waimakariri, Waimate + ECan**: the Canterbury Regional Council area minus the small Mackenzie District.
- **Hazard scenarios are modelled, not measured**: a "100-year flood" layer is a probability-based hazard envelope, not a flood map of an actual event. For historical events, check `*_historic_flood_extents` or news archives.

---

## Where to find more

- **Council datasets on eolas** (filter by cluster): [eolas.fyi/datasets](https://eolas.fyi/datasets) — use the Source filter
- **NZ local government overview**: [www.lgnz.co.nz](https://www.lgnz.co.nz) — peak body
- **Council coverage memo** (what we have, what's missing): [github.com/phildonovan/eolas — council-coverage.md](https://github.com/phildonovan/eolas/blob/main/docs/council-coverage.md)

## Related

- [LINZ source guide](linz.md) — the cadastral parcels you'll join council data to
- [Stats NZ geospatial](statsnz.md#geospatial-boundaries-census) — for boundary geographies (meshblocks, SAs, TAs)
- [Manaaki Whenua / LRIS](lris.md) — for land cover + protected areas that overlay council planning
- [Examples](../examples/index.md) — boundary mapping recipes
