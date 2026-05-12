# ECan / Canterbury Councils data via eolas

The Canterbury region covers ~670,000 people across [Environment Canterbury](https://www.ecan.govt.nz) (ECan, the regional council) and seven territorial authorities — Ashburton, Christchurch, Hurunui, Selwyn, Timaru, Waimakariri, and Waimate. eolas serves **85 datasets** spanning the region, with particularly comprehensive earthquake + flood hazard data reflecting Canterbury's recent seismic history.

If you're doing Canterbury planning, hazard, water-allocation, or post-quake property analysis — this is the source.

---

## What's in the catalogue

### Environment Canterbury (ECan) — 25 datasets

ECan is one of NZ's largest regional councils and publishes extensively. The data splits across:

| Theme | Key datasets |
|---|---|
| **Earthquake** | `ecan_earthquake_faults_2024`, `ecan_kaikoura_2016_fault_traces`, `ecan_liquefaction_polygon`, `ecan_liquefaction_susceptibility_final` |
| **Land + Water Plan (LWRP)** | `ecan_lwrp_groundwater_allocation_zones`, `ecan_lwrp_groundwater_management_zones`, `ecan_lwrp_surface_water_allocation_zones`, `ecan_lwrp_surface_water_catchments`, `ecan_lwrp_nutrient_allocation_zones` |
| **Resource consents** | `ecan_active_resource_consent_points`, `ecan_resource_consents_active_all`, `ecan_resource_consents_view` |
| **Regional Coastal Environment Plan (RCEP)** | `ecan_rcep_coastal_hazard_zones`, `ecan_rcep_significant_natural_value` |
| **Coastal + rivers** | `ecan_coastal_public_access_sites`, `ecan_coastal_natural_character_level`, `ecan_coastal_natural_character_outstanding`, `ecan_river_public_access_sites`, `ecan_tsunami_evacuation_zones` |
| **Imagery + LiDAR** | `ecan_aerial_imagery_extents`, `ecan_lidar_collection_extents` (catalogues, not the raw imagery) |
| **Other** | `ecan_district_plan_zones_consolidated` (multi-TA cross-walk), `ecan_clean_air_zones`, `ecan_historic_sites_combined`, `ecan_school_enrolment_zones` |

### Waimakariri District (WMKDC) — 29 datasets

Waimakariri publishes its full proposed District Plan 2025 layer suite:

| Pattern | Datasets |
|---|---|
| `wmkdc_dp2025_*` | New district plan overlays — designations, development areas, coastal environment, heritage, natural features, notable trees, precincts (~12 layers) |
| `wmkdc_haz_*` | Hazard layers — flood scenarios (200yr / 500yr), Ashley + Waimakariri rivers, ground shaking |
| `wmkdc_buildings`, `wmkdc_property_boundaries` | Council-published cadastral subset |

### Christchurch City Council (CCC) — 11 datasets

| Dataset | Description |
|---|---|
| `ccc_district_plan_zones` | Operative district-plan zones (post-quake recovery rebuild). |
| `ccc_district_plan_designations` | Council + Crown designations. |
| `ccc_district_plan_central_recovery` | Christchurch Central Recovery Plan overlay (post-2011 quake). |
| `ccc_district_plan_residential_character` | Residential character + scheduled areas. |
| `ccc_district_plan_scheduled_activity` | Specific activity-scheduled sites. |
| `ccc_district_plan_liquefaction_mgmt` | Liquefaction management overlay — different from ECan's regional layer. |
| `ccc_coastal_erosion_hazard`, `ccc_coastal_inundation_hazard` | Coastal hazards. |
| `ccc_cycleway_network` | Christchurch's cycle network. |

### Ashburton District (ashb) — 16 datasets

Comprehensive coverage: zones, designations, flood / fault / geoconservation hazards, heritage, irrigation designations, railway, stopbanks, water bodies.

### Hurunui District — 4 datasets

Basic coverage: designations, district plan zones, heritage, flood hazards.

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Most Canterbury councils publish via [opendata.canterburymaps.govt.nz](https://opendata.canterburymaps.govt.nz) — a shared Koordinates portal — plus their own ArcGIS portals. ECan also publishes its own layers via [ecan.govt.nz/data](https://www.ecan.govt.nz/data).

The Waimakariri District Plan 2025 layers update as the plan moves through hearings + decisions; the suffix `_decision` (where present) tracks the post-decisions version.

```python
meta = client.info("ecan_earthquake_faults_2024")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Canterbury council data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: [Council name], served via eolas (eolas.fyi). CC-BY 4.0."* — substitute ECan / CCC / WMKDC etc. as applicable.

---

## Common patterns

### Post-quake property due diligence (Christchurch)

The Canterbury-specific workflow that became routine after 2010-2011:

=== "Python"

    ```python
    import geopandas as gpd
    from shapely.geometry import Point

    pt = gpd.GeoSeries([Point(172.6362, -43.5321)], crs="EPSG:4326")  # central Christchurch

    layers = {
        "Liquefaction (CCC)": "ccc_district_plan_liquefaction_mgmt",
        "Liquefaction (ECan regional)": "ecan_liquefaction_polygon",
        "Fault avoidance": "ecan_earthquake_faults_2024",
        "Coastal erosion": "ccc_coastal_erosion_hazard",
        "Coastal inundation": "ccc_coastal_inundation_hazard",
    }
    for label, name in layers.items():
        layer = client.canterbury(name, as_sf=True)
        hit = gpd.sjoin(pt.to_frame("g").set_geometry("g"), layer, predicate="within")
        print(f"  {label}: {'YES' if len(hit) else 'no'}")
    ```

=== "R"

    ```r
    library(sf)
    pt <- st_sfc(st_point(c(172.6362, -43.5321)), crs = 4326)

    layers <- c(
      "Liquefaction (CCC)"    = "ccc_district_plan_liquefaction_mgmt",
      "Liquefaction (ECan)"   = "ecan_liquefaction_polygon",
      "Fault avoidance"       = "ecan_earthquake_faults_2024"
    )

    for (label in names(layers)) {
      layer <- eolas_get_canterbury(layers[label], as_sf = TRUE)
      cat(label, ":", any(st_within(pt, layer, sparse = FALSE)), "\n")
    }
    ```

### Water allocation: surface vs groundwater

ECan administers Canterbury's contested water resource — useful for irrigation, dairy, and resource-consent analysis:

```python
import geopandas as gpd

gw = client.canterbury("ecan_lwrp_groundwater_allocation_zones", as_sf=True)
sw = client.canterbury("ecan_lwrp_surface_water_allocation_zones", as_sf=True)

# Active surface-water takes per zone
consents = client.canterbury("ecan_active_resource_consent_points", as_sf=True)
water_takes = consents[consents["consent_type"].str.contains("water take", case=False, na=False)]
takes_by_zone = gpd.sjoin(water_takes, sw, predicate="within").groupby("zone_name").size()
print(takes_by_zone.sort_values(ascending=False).head(15))
```

### Earthquake fault buffers

```python
import geopandas as gpd

faults = client.canterbury("ecan_earthquake_faults_2024", as_sf=True).to_crs("EPSG:2193")
faults["buffer_20m"] = faults.geometry.buffer(20)
# Properties within 20m of a fault — typically subject to building-setback rules
```

---

## Source-specific notes

- **Two liquefaction layers exist**: `ccc_district_plan_liquefaction_mgmt` is Christchurch City's *planning* layer (drives consenting rules); `ecan_liquefaction_polygon` is ECan's regional *hazard* layer (broader scientific assessment). They mostly overlap but aren't identical — for consenting, use the CCC layer; for risk assessment, use ECan's.
- **Post-quake Canterbury data is dense for a reason**: the 2010-2011 sequence + 2016 Kaikōura quake generated enormous post-event data. `ecan_kaikoura_2016_fault_traces` captures observed surface ruptures; `ecan_earthquake_faults_2024` is the current legally-recognised hazard envelope.
- **Christchurch Central Recovery Plan**: a unique post-quake regulatory overlay specific to central Christchurch. Different consenting rules apply within it.
- **WMKDC's two plan generations**: the *operative* district plan is the current legal document; the *DP2025* layers (`wmkdc_dp2025_*`) are the proposed plan in hearings. Both serve different purposes — use the operative for active consenting, DP2025 for forecasting.
- **Hurunui + Selwyn coverage**: limited but growing. As both councils publish more open data, eolas will add layers — see [eolas.fyi/datasets?source=ECan+%2F+Canterbury](https://eolas.fyi/datasets?source=ECan%20%2F%20Canterbury) for the current list.
- **Selwyn, Timaru, Waimate**: minimal layers via the cluster's shared Koordinates portal. Their own portals have more — on the eolas roadmap to fold in.
- **Aerial imagery + LiDAR**: `ecan_aerial_imagery_extents` + `ecan_lidar_collection_extents` are *catalogues* (where coverage exists, when flown) — not the raw imagery / point clouds themselves. Raw data is available via ECan's portal on request.

---

## Where to find more

- **Canterbury datasets on eolas**: [eolas.fyi/datasets?source=ECan+%2F+Canterbury](https://eolas.fyi/datasets?source=ECan%20%2F%20Canterbury)
- **Canterbury Maps Open Data** (the shared portal): [opendata.canterburymaps.govt.nz](https://opendata.canterburymaps.govt.nz)
- **ECan data + science**: [www.ecan.govt.nz/data](https://www.ecan.govt.nz/data)
- **CCC GeoMaps**: [opendata.ccc.govt.nz](https://opendata.ccc.govt.nz)

## Related

- [Councils overview](councils.md) — the full council coverage model
- [LINZ](linz.md) — for cadastral parcels you'll join hazards to (Canterbury post-quake LINZ data is well-maintained)
- [Examples](../examples/index.md) — boundary mapping recipes
