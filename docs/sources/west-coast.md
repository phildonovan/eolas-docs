# West Coast (Te Tai o Poutini) data via eolas

The West Coast region covers ~33,000 people across [West Coast Regional Council](https://www.wcrc.govt.nz) (WCRC) and three territorial authorities — Buller, Grey, and Westland. All three TAs share a single common district plan: **Te Tai o Poutini Plan (TTPP)**. eolas serves **24 datasets** for the cluster.

If you're doing West Coast property research, mining / extractive consenting, or alpine / coastal hazard work — this is the source.

---

## What's in the catalogue

| Source | Code | Datasets | Notes |
|---|---|---|---|
| Te Tai o Poutini Plan (shared) | ttpp | 12 | Combined district plan covering all three TAs |
| WCRC | wcrc | 8 | Regional planning, hazards, environmental |
| Buller District (specific) | buller | 3 | Council-specific extras |
| Westland District (specific) | westland | 1 | Council-specific extra |

### TTPP (Te Tai o Poutini Plan) datasets

The shared plan layers — apply across Buller + Grey + Westland:

- `ttpp_archaeological_areas`
- `ttpp_designations`
- `ttpp_district_plan_zones`
- `ttpp_fault_avoidance_zone` (Alpine Fault + others)
- `ttpp_flood_hazard_severe`, `ttpp_flood_susceptibility`
- `ttpp_heritage_sites_polygon`
- `ttpp_outstanding_natural_features`, `ttpp_outstanding_natural_landscapes`
- `ttpp_significant_natural_areas`
- `ttpp_sites_significance_maori`
- `ttpp_tsunami_hazard_zone`

### WCRC + council-specific

- WCRC publishes regional environmental + planning layers (8 datasets)
- `buller_*` (3 datasets) — Buller-specific overlays
- `westland_*` (1 dataset) — Westland-specific extra

Browse: [eolas.fyi/datasets?source=West+Coast+%28Te+Tai+o+Poutini%29](https://eolas.fyi/datasets?source=West%20Coast%20%28Te%20Tai%20o%20Poutini%29).

---

## Refresh schedule

Weekly, Wednesday morning NZ time.

---

## License

All West Coast council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

---

## Common patterns

### Alpine Fault avoidance

```python
import geopandas as gpd
fault = client.west_coast("ttpp_fault_avoidance_zone", as_sf=True)
print(f"Fault-avoidance polygons: {len(fault)}")
print(f"Total area: {fault.to_crs('EPSG:2193').area.sum() / 1e6:.0f} km²")
```

### District plan zone composition

```python
zones = client.west_coast("ttpp_district_plan_zones", as_sf=True)
print(zones["zone_name"].value_counts().head(10))
```

---

## Source-specific notes

- **Shared plan, three councils**: Te Tai o Poutini Plan is unusual in NZ — most councils each have their own DP. Here Buller, Grey, and Westland operate a single shared plan, simplifying cross-district analysis.
- **Alpine Fault**: the entire West Coast sits next to one of NZ's most-active faults — fault-avoidance zones are a major planning constraint.
- **Tsunami exposure**: the West Coast has significant tsunami risk from local + distant sources; `ttpp_tsunami_hazard_zone` covers the exposure.
- **Mining / extractive context**: West Coast has significant historical + ongoing coal + gold mining. Some council layers (not yet in eolas) cover mining-related overlays.
- **Limited urban coverage**: Greymouth, Westport, Hokitika are small — most of the region is forest + farmland + mining. Layer counts reflect that.

---

## Where to find more

- **West Coast datasets on eolas**: [eolas.fyi/datasets?source=West+Coast+%28Te+Tai+o+Poutini%29](https://eolas.fyi/datasets?source=West%20Coast%20%28Te%20Tai%20o%20Poutini%29)
- **Te Tai o Poutini Plan**: [www.ttpp.nz](https://www.ttpp.nz)
- **WCRC**: [www.wcrc.govt.nz](https://www.wcrc.govt.nz)

## Related

- [Councils overview](councils.md) | [Examples](../examples/index.md)
