# Auckland Council data via eolas

[Auckland Council](https://www.aucklandcouncil.govt.nz) is the country's only super-city — a unitary authority covering 1.7M people across Auckland, Manukau, Waitakere, North Shore and Rodney. eolas serves **20 datasets** from Auckland Council — focused on the Auckland Unitary Plan (AUP) overlays that drive every property, planning, and consent decision in the region.

If you're doing Auckland property research, planning analysis, or hazard / heritage / mana whenua due diligence — this is the source.

For transport data (bus routes, ferries, cycle network), see the separate [Auckland Transport guide](auckland-transport.md).

---

## What's in the catalogue

### Auckland Unitary Plan overlays

Most layers are AUP "overlays" — areas where additional planning rules apply on top of the underlying zone.

| Dataset | Description |
|---|---|
| `akc_historic_heritage_overlay_extent_of_place` | Scheduled heritage areas — broader curtilage including context. |
| `akc_historic_heritage_overlay_place` | Scheduled heritage places — individual buildings, items, structures. |
| `akc_special_character_areas_overlay` | Special-character residential or business areas (e.g. Devonport, Mount Eden, Ponsonby). |
| `akc_significant_ecological_areas_overlay` | Ecologically significant areas (SEAs) — biodiversity protection. |
| `akc_notable_trees_overlay` | Individual notable trees. |
| `akc_notable_group_of_trees_overlay` | Notable tree groups. |
| `akc_outstanding_natural_features_overlay` | ONFs — geological / landscape features of outstanding value. |
| `akc_outstanding_natural_landscapes_overlay` | ONLs — outstanding natural landscapes (e.g. parts of the Waitakere Ranges). |
| `akc_outstanding_natural_character_overlay` | Coastal character protection. |
| `akc_sites_of_significance_to_mana_whenua_overlay` | Sites of significance to iwi / hapū (locations + boundaries published with iwi consent). |

### Hazards + infrastructure

| Dataset | Description |
|---|---|
| `akc_aircraft_noise_overlay` | Airport noise contours (AIANB, ANB1-3) — relevant for residential consenting near AIA. |
| `akc_national_grid_corridor_overlay` | Transpower national grid corridor — yard / building setback rules apply. |
| `akc_quarry_buffer_area_overlay` | Buffers around active quarries (noise + dust). |
| `akc_high_use_aquifer_management_areas` | Aquifers under sustained use — water-take rules apply. |
| `akc_quality_sensitive_aquifer_management_areas` | Aquifers vulnerable to contamination — discharge rules apply. |

Plus 5 additional AUP overlays. Browse [eolas.fyi/datasets?source=Auckland+Council](https://eolas.fyi/datasets?source=Auckland%20Council) for the full list.

---

## Refresh schedule

Weekly, Wednesday morning NZ time. Auckland Council publishes via the [GeoMaps Open Data Portal](https://data-aucklandcouncil.opendata.arcgis.com) (ArcGIS). The AUP overlays update when plan changes are notified or operative — typically a few times per year, occasionally a flurry of changes during plan reviews.

```python
meta = client.info("akc_historic_heritage_overlay_place")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Auckland Council data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Auckland Council, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### What overlays apply at a location?

The classic "due diligence on a property" workflow:

=== "Python"

    ```python
    import geopandas as gpd
    from shapely.geometry import Point

    pt = gpd.GeoSeries([Point(174.7633, -36.8485)], crs="EPSG:4326")  # central Auckland

    # Load every Auckland overlay and check which contain this point
    overlays = [
        "akc_historic_heritage_overlay_place",
        "akc_special_character_areas_overlay",
        "akc_significant_ecological_areas_overlay",
        "akc_outstanding_natural_features_overlay",
        "akc_outstanding_natural_landscapes_overlay",
        "akc_aircraft_noise_overlay",
        "akc_national_grid_corridor_overlay",
    ]
    hits = []
    for name in overlays:
        layer = client.auckland_council(name, as_sf=True)
        hit = gpd.sjoin(pt.to_frame("geom").set_geometry("geom"), layer, predicate="within")
        if len(hit):
            hits.append(name)

    print("Overlays affecting this point:", hits)
    ```

=== "R"

    ```r
    library(sf)
    library(dplyr)

    pt <- st_sfc(st_point(c(174.7633, -36.8485)), crs = 4326)

    overlays <- c(
      "akc_historic_heritage_overlay_place",
      "akc_special_character_areas_overlay",
      "akc_significant_ecological_areas_overlay"
    )

    hits <- c()
    for (name in overlays) {
      layer <- eolas_get_auckland_council(name, as_sf = TRUE)
      if (any(st_within(pt, layer, sparse = FALSE))) hits <- c(hits, name)
    }
    print(hits)
    ```

### Heritage register growth

```python
heritage = client.auckland_council("akc_historic_heritage_overlay_place", as_sf=True)
# Schedule column carries the scheduling year for most entries
by_year = heritage.groupby("schedule_year").size().sort_index()
by_year.plot(kind="bar", title="Auckland heritage scheduling by year")
```

### Special-character area composition

```python
sca = client.auckland_council("akc_special_character_areas_overlay", as_sf=True)
print(sca["area_name"].value_counts().head(10))
# Devonport, Mount Eden, Ponsonby, Grey Lynn, Sandringham, ...
```

---

## Source-specific notes

- **Auckland is a unitary authority**: it does both TA and regional council functions. Some layers (aquifer management, coastal areas) that you'd find on a regional council elsewhere are on Auckland Council here.
- **AUP is the legal document, the overlays are the data**: an overlay is the geospatial expression of an AUP rule. The legal weight lives in the AUP text itself ([unitaryplan.aucklandcouncil.govt.nz](https://unitaryplan.aucklandcouncil.govt.nz)) — overlays in eolas are the spatial precise-location reference.
- **Mana whenua sites are pre-redacted**: locations published in `akc_sites_of_significance_to_mana_whenua_overlay` have iwi consent. Some sensitive sites are deliberately published as broader polygons rather than exact points; treat the published geometry as authoritative.
- **Schedule numbers vary by overlay**: heritage places are individually-numbered (Schedule 14.1, 14.2, ...). Special character areas are area-named, not numbered. Tree overlays use unique IDs per tree/group.
- **Auckland Transport is separate**: bus / ferry / train / cycle data is in [Auckland Transport](auckland-transport.md), not Auckland Council.
- **Not in eolas (yet)**: stormwater overland flow paths (very large + frequently revised), parcel-level zoning maps (use AUP base zone overlay separately), individual consent decisions (case-by-case).

---

## Where to find more

- **Auckland Council datasets on eolas**: [eolas.fyi/datasets?source=Auckland+Council](https://eolas.fyi/datasets?source=Auckland%20Council)
- **Auckland Council GeoMaps Open Data**: [data-aucklandcouncil.opendata.arcgis.com](https://data-aucklandcouncil.opendata.arcgis.com)
- **Auckland Unitary Plan** (the legal document): [unitaryplan.aucklandcouncil.govt.nz](https://unitaryplan.aucklandcouncil.govt.nz)
- **Auckland Council GeoMaps** (interactive map): [geomapspublic.aucklandcouncil.govt.nz](https://geomapspublic.aucklandcouncil.govt.nz)

## Related

- [Auckland Transport](auckland-transport.md) — bus / ferry / cycle / train data
- [LINZ](linz.md) — for the underlying cadastral parcels you'll join overlays to
- [Councils overview](councils.md) — the full council coverage model
- [Examples](../examples/index.md) — boundary mapping recipes
