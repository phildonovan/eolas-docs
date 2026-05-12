# DOC data via eolas

The [Department of Conservation](https://www.doc.govt.nz) (DOC) manages New Zealand's ~8.8 million hectares of public conservation land — about a third of the country — plus the network of huts, campsites, and tracks that sit on it. eolas serves **10 datasets** from DOC: the canonical layers behind every "find a hut", "where can I camp", and "what's protected" workflow.

If you're building outdoor / tramping / tourism tools, doing conservation-policy analysis, or producing recreation reports — DOC is the source.

---

## What's in the catalogue

### Recreation infrastructure

| Dataset | Description |
|---|---|
| `doc_huts` | All ~1,400 DOC huts (backcountry, serviced, basic, historic). Point geometry + facilities + bookable flag. |
| `doc_campsites` | All ~300 DOC-managed campsites (basic / standard / scenic / serviced). Point geometry + facilities + booking system. |
| `doc_tracks` | All ~3,200 walking, tramping, and back-country tracks. Polyline geometry + length, difficulty, status. |
| `doc_walking_experiences_locations` | Curated "experience" point locations — the marketing-quality subset of tracks/huts featured on DOC's visitor-facing site. |
| `doc_walking_experiences_routes` | Polyline routes for the same curated experiences. Pair with `_locations` for the full set. |

### Protected areas

| Dataset | Description |
|---|---|
| `doc_public_conservation_land` | ~11,000 parcels of public conservation land — national parks, conservation parks, ecological areas, reserves. |
| `doc_marine_reserves` | All gazetted marine reserves under the Marine Reserves Act 1971, plus indicative areas. |
| `doc_marine_mammal_sanctuaries` | Boundaries of gazetted marine mammal sanctuaries (e.g. Banks Peninsula, Te Pewhairangi/Bay of Islands). |

### Operational alerts (current closures + warnings)

| Dataset | Description |
|---|---|
| `operational_alerts_campsites` | Current alerts on campsites — temporary closures, facility outages, access advisories. |
| `operational_alerts_huts` | Current alerts on huts — closures, water-supply outages, track damage. |

---

## Refresh schedule

Weekly, Wednesday morning NZ time.

The recreation-infrastructure layers (huts, campsites, tracks) update from DOC's authoritative system as new bookings go live or assets are added. The operational-alerts feeds refresh weekly but the source is updated daily — for absolutely up-to-the-minute closures, also check the [DOC alerts page](https://www.doc.govt.nz/parks-and-recreation/places-to-go/alerts) before trips.

```python
meta = client.info("doc_huts")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All DOC data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)** via the [DOC Open Data Portal](https://doc-deptconservation.opendata.arcgis.com). Commercial use is fine; attribution required.

Recommended attribution: *"Source: Department of Conservation, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### All huts in Fiordland

=== "Python"

    ```python
    import geopandas as gpd

    huts = client.doc("doc_huts", as_sf=True)
    # Filter to Fiordland National Park (most DOC layers tag region/conservancy)
    fiordland = huts[huts["region"] == "Southland"]
    fiordland.plot(figsize=(8, 10), markersize=10)
    ```

=== "R"

    ```r
    library(sf)
    library(ggplot2)

    huts <- eolas_get_doc("doc_huts", as_sf = TRUE)
    fiordland <- huts[huts$region == "Southland", ]

    ggplot(fiordland) + geom_sf(size = 0.6) + theme_void() +
      labs(title = "Southland DOC huts")
    ```

### Active closures for trip planning

```python
hut_alerts = client.doc("operational_alerts_huts")
camp_alerts = client.doc("operational_alerts_campsites")

# Active alerts in the Tongariro region this week
import pandas as pd
all_alerts = pd.concat([hut_alerts, camp_alerts])
tongariro = all_alerts[all_alerts["region"].str.contains("Tongariro", case=False, na=False)]
print(tongariro[["asset_name", "alert_type", "summary"]].to_string())
```

### Track network length by region

```python
tracks = client.doc("doc_tracks", as_sf=True)
# `tracks_meters` exists; if not, compute from geometry
tracks["length_km"] = tracks.to_crs("EPSG:2193").length / 1000
by_region = tracks.groupby("region")["length_km"].sum().sort_values(ascending=False)
print(by_region.head(10))
```

### Marine protection overlay

```python
import geopandas as gpd

reserves = client.doc("doc_marine_reserves", as_sf=True)
mammals = client.doc("doc_marine_mammal_sanctuaries", as_sf=True)

# Total area protected (km²)
print("Marine reserves:", reserves.to_crs("EPSG:2193").area.sum() / 1e6, "km²")
print("Marine mammal sanctuaries:", mammals.to_crs("EPSG:2193").area.sum() / 1e6, "km²")
```

---

## Source-specific notes

- **Walking experiences vs tracks**: `doc_walking_experiences_*` is a curated subset of `doc_tracks` (the marketing-quality "Great Walks" + featured tramps). For a complete network, use `doc_tracks`; for the consumer-friendly set with photos and route narratives on DOC's site, use the experiences pair.
- **PCL is a parcel layer**: `doc_public_conservation_land` is ~11k discrete parcels, not 13 national-park polygons. To analyse "national park X total area", aggregate by the `legal_status` or `park_name` field.
- **Booking flag ≠ everything bookable**: `is_bookable` on huts/campsites is DOC's booking-system flag. Some seasonal sites take payment via honesty box (no online booking) and are flagged false despite being usable.
- **Geometry**: all DOC datasets expose `geometry_wkt`; use `as_sf=True` (Python) or `as_sf = TRUE` (R) to get a GeoDataFrame / sf object.
- **Marine reserves overlap with LINZ**: DOC publishes the legal boundaries (`doc_marine_reserves`); for the underlying coastline/seabed/EEZ, use [LINZ](linz.md). For a "where can I fish?" analysis you typically want both.
- **Crown vs DOC land**: not all Crown-owned land is DOC-managed — pastoral leases, defence land, river/lake beds are Crown but outside `doc_public_conservation_land`.

---

## Where to find more

- **DOC datasets on eolas**: [eolas.fyi/datasets?source=DOC](https://eolas.fyi/datasets?source=DOC)
- **DOC Open Data Portal**: [doc-deptconservation.opendata.arcgis.com](https://doc-deptconservation.opendata.arcgis.com)
- **DOC alerts (live)**: [www.doc.govt.nz/parks-and-recreation/places-to-go/alerts](https://www.doc.govt.nz/parks-and-recreation/places-to-go/alerts)
- **DOC booking system**: [bookings.doc.govt.nz](https://bookings.doc.govt.nz)

## Related

- [LINZ source guide](linz.md) — for the underlying topographic + coastline layers
- [Manaaki Whenua / LRIS source guide](lris.md) — for the Land Cover Database + protected-areas network (covers DOC + private QEII covenants + iwi-protected)
- [Examples](../examples/index.md) — boundary mapping recipes
