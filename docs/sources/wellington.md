# Wellington Region Councils data via eolas

The Wellington region covers ~540,000 people across [Greater Wellington Regional Council](https://www.gw.govt.nz) (GWRC) and eight territorial authorities — Carterton, Hutt, Kāpiti, Masterton, Porirua, South Wairarapa, Upper Hutt, and Wellington City. eolas serves **76 datasets** spanning the region — every council's district plan, hazard layers, and the regional council's environmental + transport data.

If you're doing Wellington-region property research, hazard analysis, planning work, or earthquake / coastal exposure modelling — this is the source. Wellington has particularly comprehensive hazard data because of its earthquake + tsunami + flood exposure.

---

## What's in the catalogue

### Greater Wellington Regional Council (GWRC) — 21 datasets

Regional-scale environmental + transport data:

| Theme | Datasets |
|---|---|
| Hazards | `gwrc_flood_hazard_extents`, `gwrc_eq_urm_buildings` (unreinforced masonry buildings at risk) |
| Coastal | `gwrc_coastline_mhws10` (mean-high-water-springs +10cm — sea-level-rise reference) |
| Environment | `gwrc_key_native_ecosystems`, `gwrc_groundwater_zones`, `gwrc_river_flows_p` (recorder sites), `gwrc_sites_of_significance_mana_whenua` |
| Transport | `gwrc_metlink_park_and_ride`, `gwrc_regional_cycle_network` |
| Land + planning | `gwrc_regional_parks_forests`, `gwrc_managed_land_wairarapa`, `gwrc_nrp_operative` (Natural Resources Plan operative), `gwrc_nrp_plan_change_1` (proposed) |
| Operations | `gwrc_resource_consents`, `gwrc_predator_free_phase2` |

### Wellington City Council (WCC) — 9 datasets

| Dataset | Description |
|---|---|
| `wcc_district_plan_zones_2024` | Operative district plan zones (post-2024 plan review). |
| `wcc_flood_hazard_operative`, `wcc_coastal_inundation_operative`, `wcc_coastal_tsunami_operative`, `wcc_liquefaction_operative` | Hazard layers in the operative plan. |
| `wcc_significant_natural_areas` | SNAs — biodiversity protection. |

### Wellington City proposed district plan (WCDP) — 10 datasets

Wellington City's *new* district plan (in late-stage consultation / hearings):

| Dataset | Description |
|---|---|
| `wcdp_*_decision` | "Decisions version" of various overlays — airport obstacle limits, fault hazards, flood, heritage precincts, heritage sites, etc. |

### Porirua City Council (PCC) — 10 datasets

| Theme | Datasets |
|---|---|
| Planning | `pcc_district_plan_zones`, `pcc_designations` |
| Hazards | `pcc_flood_overland_flow`, `pcc_flood_ponding`, `pcc_flood_stream_corridor`, `pcc_coastal_future_inundation_1m_slr` |

### Hutt City Council (HuttCC) — 8 datasets

| Dataset | Description |
|---|---|
| `huttcc_flood_hazard_overlay`, `huttcc_flood_100yr_groundwater` | Flood + groundwater-driven flooding (Hutt valley specific). |
| `huttcc_coastal_inundation_overlay`, `huttcc_coastal_tsunami_overlay` | Coastal hazards. |
| `huttcc_designations`, `huttcc_heritage_areas` | Planning overlays. |

### Kāpiti Coast (KCDC) — 7 datasets

| Dataset | Description |
|---|---|
| `kcdc_district_plan_zones`, `kcdc_district_plan_precincts` | Operative district plan structure. |
| `kcdc_designations_kcdc`, `kcdc_designations_nzta` | Designations (council + NZTA). |
| `kcdc_flood_extents`, `kcdc_ecological_sites` | Hazards + biodiversity. |

### Upper Hutt City Council (UHCC) — 7 datasets

District plan zones + hazard suite (flood, slope, erosion) — mirrors the structure of other regional TAs.

### Masterton District Council — 4 datasets

| Dataset | Description |
|---|---|
| `masterton_earthquake_hazards` | Earthquake hazards (Wellington Fault runs through Masterton). |
| `masterton_flood_zones`, `masterton_liquefaction`, `masterton_tsunami_evac` | Hazard layers. |

Plus smaller suites from Carterton + South Wairarapa.

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Each council publishes via its own portal — GWRC via Koordinates, Wellington City via [data.wellingtoncc.govt.nz](https://data.wellingtoncc.govt.nz), and most district councils via ArcGIS. The pipeline pulls from each source independently.

```python
meta = client.info("gwrc_flood_hazard_extents")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Wellington-region council data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; per-council attribution required.

Recommended attribution: *"Source: [Council name], served via eolas (eolas.fyi). CC-BY 4.0."* — use the specific council; for multi-council analysis: *"Source: Wellington-region councils via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Earthquake + tsunami exposure for a property

The Wellington-specific due-diligence workflow:

=== "Python"

    ```python
    import geopandas as gpd
    from shapely.geometry import Point

    pt = gpd.GeoSeries([Point(174.7762, -41.2865)], crs="EPSG:4326")  # central Wellington

    # WCC operative liquefaction + tsunami overlays
    liq = client.wellington("wcc_liquefaction_operative", as_sf=True)
    tsu = client.wellington("wcc_coastal_tsunami_operative", as_sf=True)

    in_liq = gpd.sjoin(pt.to_frame("g").set_geometry("g"), liq, predicate="within")
    in_tsu = gpd.sjoin(pt.to_frame("g").set_geometry("g"), tsu, predicate="within")
    print(f"Liquefaction zone: {len(in_liq) > 0}")
    print(f"Tsunami evacuation zone: {len(in_tsu) > 0}")
    ```

=== "R"

    ```r
    library(sf)
    library(dplyr)

    pt <- st_sfc(st_point(c(174.7762, -41.2865)), crs = 4326)
    liq <- eolas_get_wellington("wcc_liquefaction_operative", as_sf = TRUE)
    tsu <- eolas_get_wellington("wcc_coastal_tsunami_operative", as_sf = TRUE)

    cat("Liquefaction:", any(st_within(pt, liq, sparse = FALSE)), "\n")
    cat("Tsunami evac:", any(st_within(pt, tsu, sparse = FALSE)), "\n")
    ```

### URM (unreinforced masonry) buildings in the region

Wellington has a known earthquake-prone URM building stock — GWRC publishes the register:

```python
urm = client.wellington("gwrc_eq_urm_buildings", as_sf=True)
print(f"URM buildings: {len(urm)}")
# By TA
print(urm.groupby("ta_name").size().sort_values(ascending=False))
```

### Compare operative vs proposed plan zones (WCC)

```python
operative = client.wellington("wcc_district_plan_zones_2024", as_sf=True)
proposed_decisions = client.wellington("wcdp_amenity_landscapes_decision", as_sf=True)
# Differences are where the proposed plan changes the AUP rule
```

---

## Source-specific notes

- **GWRC ≠ Wellington City Council**: GWRC is the regional council (environment, transport, flood protection at regional scale). Wellington City is one of nine TAs within the GWRC area. Both publish data — don't confuse them.
- **Wellington City has two plans in eolas**: `wcc_*_operative` (current legal plan, in effect) + `wcdp_*_decision` (proposed plan, late-stage consultation as at refresh time). The proposed plan will eventually replace the operative; both are kept while transition is in progress.
- **URM building register is privacy-sensitive at address level**: GWRC publishes building locations + status. Some owners have applied for exemptions or are mid-remediation; don't infer present-day status from a snapshot without checking the date.
- **Hazard mapping methodology varies**: WCC's flood overlay uses 100-yr return-period modelling; Porirua's uses 100yr + 200yr scenarios; KCDC uses a different modelling methodology. Don't directly compare hazard counts across councils without normalising for methodology.
- **Wellington Fault**: runs along the western edge of the harbour through Hutt + Masterton. The `*_fault_*` overlays (where present) mark setback zones around the trace.
- **Coastal SLR scenarios**: PCC publishes a `_1m_slr` (1m sea-level-rise) layer reflecting central RCP4.5 projections; other councils use different SLR assumptions. Inspect the metadata before cross-council coastal-risk analysis.

---

## Where to find more

- **Wellington-region datasets on eolas**: [eolas.fyi/datasets?source=Wellington+Region+Councils](https://eolas.fyi/datasets?source=Wellington%20Region%20Councils)
- **GWRC data portal**: [data.gw.govt.nz](https://data.gw.govt.nz)
- **WCC data portal**: [data.wellingtoncc.govt.nz](https://data.wellingtoncc.govt.nz)
- **District-plan portals**: each council has its own — check the council's website

## Related

- [Councils overview](councils.md) — the full council coverage model
- [LINZ](linz.md) — for the cadastral parcels you'll join hazard data to
- [Examples](../examples/index.md) — boundary mapping recipes
