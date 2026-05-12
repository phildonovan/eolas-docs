# Auckland Transport data via eolas

[Auckland Transport](https://at.govt.nz) (AT) operates Auckland's public transport network — bus, ferry, train, plus the cycle network and park-and-ride facilities. eolas serves **10 datasets** from AT — the spatial layers behind every "how do I get from A to B" query in Auckland.

If you're doing transport-planning, mode-share analysis, accessibility studies, or building a transit-aware Auckland app — this is the source.

For Auckland's *planning* data (district plan, hazards, heritage), see [Auckland Council](auckland-council.md). AT is a separate Council-Controlled Organisation (CCO) with its own data portal.

---

## What's in the catalogue

### Public transport

| Dataset | Description |
|---|---|
| `akt_bus_route` | All AT bus routes — polyline geometry + route number, direction. |
| `akt_bus_stop` | All AT bus stops — point geometry + accessibility flags, shelter info. |
| `akt_school_bus_route` | School bus routes (separate from regular network). |
| `akt_school_bus_stop` | School bus stops. |
| `akt_ferry_route` | Ferry routes — polyline + operator, service frequency. |
| `akt_ferry_stop` | Ferry terminals + landings — point. |
| `akt_train_station` | Train stations — point geometry + platforms, parking, accessibility. |
| `akt_park_and_ride` | Park-and-ride facilities — point + capacity, mode connections. |

### Active modes

| Dataset | Description |
|---|---|
| `akt_cycle_facility_network` | All Auckland cycle network infrastructure — separated paths, shared paths, on-road lanes, sharrows. |
| `akt_bridges` | Bridges in the AT-managed road network. |

---

## Refresh schedule

Weekly, Wednesday morning NZ time. AT publishes via the [AT Open Data Portal](https://data-atgis.opendata.arcgis.com) (ArcGIS).

Bus routes and stops can change quarterly with service reviews; the cycle network grows as new infrastructure is built (typically several updates per year). Train stations are stable; ferry routes change rarely.

For real-time transit data (vehicle locations, arrival predictions), use [AT's GTFS-RT feed](https://dev-portal.at.govt.nz) — not in eolas.

```python
meta = client.info("akt_bus_route")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All AT data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Auckland Transport, served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Plot the entire Auckland network

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    buses = client.auckland_transport("akt_bus_route", as_sf=True)
    trains = client.auckland_transport("akt_train_station", as_sf=True)
    ferries = client.auckland_transport("akt_ferry_route", as_sf=True)
    cycle = client.auckland_transport("akt_cycle_facility_network", as_sf=True)

    fig, ax = plt.subplots(figsize=(10, 12))
    buses.plot(ax=ax, color="lightblue", linewidth=0.4, label="Bus")
    cycle.plot(ax=ax, color="green", linewidth=0.6, label="Cycle")
    ferries.plot(ax=ax, color="navy", linewidth=1.0, label="Ferry")
    trains.plot(ax=ax, color="red", markersize=20, label="Train station")
    ax.set_title("Auckland public transport network")
    ax.legend()
    plt.show()
    ```

=== "R"

    ```r
    library(sf)
    library(ggplot2)

    buses <- eolas_get_auckland_transport("akt_bus_route", as_sf = TRUE)
    trains <- eolas_get_auckland_transport("akt_train_station", as_sf = TRUE)
    cycle <- eolas_get_auckland_transport("akt_cycle_facility_network", as_sf = TRUE)

    ggplot() +
      geom_sf(data = buses, linewidth = 0.2, colour = "lightblue") +
      geom_sf(data = cycle, linewidth = 0.5, colour = "green") +
      geom_sf(data = trains, size = 1.5, colour = "red") +
      theme_void() +
      labs(title = "Auckland PT network")
    ```

### Bus-stop accessibility for a property

```python
import geopandas as gpd
from shapely.geometry import Point

# Walking accessibility = bus stops within 400m of a point
pt = gpd.GeoSeries([Point(174.7633, -36.8485)], crs="EPSG:4326").to_crs("EPSG:2193")
stops = client.auckland_transport("akt_bus_stop", as_sf=True).to_crs("EPSG:2193")

nearby = stops[stops.geometry.distance(pt.iloc[0]) <= 400]
print(f"Bus stops within 400m: {len(nearby)}")
```

### Cycle-network density by suburb

```python
import geopandas as gpd

cycle = client.auckland_transport("akt_cycle_facility_network", as_sf=True)
suburbs = client.linz("nz_suburbs_and_localities", as_sf=True)
# Cycle km per suburb
cycle = cycle.to_crs("EPSG:2193")
cycle["length_m"] = cycle.geometry.length
suburb_with_cycle = gpd.sjoin(cycle, suburbs, how="inner", predicate="intersects")
top = suburb_with_cycle.groupby("name")["length_m"].sum().sort_values(ascending=False).head(15)
print(top.div(1000).round(1).astype(str) + " km")
```

---

## Source-specific notes

- **AT is a CCO, not the Council**: data ownership + publication is separate from Auckland Council. AT also runs the road network (AT-managed roads), shoulder of NZTA state highways within Auckland.
- **Routes vs services vs trips**: `akt_bus_route` is the *spatial* route a service follows. Frequency, timetable, and live arrivals are in the GTFS feed (not in eolas) — they reference a `route_id` that matches AT's GTFS data.
- **Cycle-facility types**: the `facility_type` field distinguishes separated paths (most common in recent infrastructure), shared paths, on-road lanes, and sharrows (shared with cars). Don't treat them as equivalent for accessibility analysis.
- **Stops + stations have accessibility flags**: `wheelchair_accessible`, `shelter`, `bike_parking`, etc. Useful for equity-of-access analysis.
- **Not in eolas**: GTFS schedule data, GTFS-RT (real-time), HOP card usage stats. AT publishes GTFS at [dev-portal.at.govt.nz](https://dev-portal.at.govt.nz) — better suited as a streaming dataset than a batch table.
- **Train stations are operated by AT but the rail network is KiwiRail's**: AT owns Britomart + most platforms; the lines/signals are KiwiRail. For the rail line geometry (where the tracks actually run), use [LINZ rail centrelines](linz.md).

---

## Where to find more

- **Auckland Transport datasets on eolas**: [eolas.fyi/datasets?source=Auckland+Transport](https://eolas.fyi/datasets?source=Auckland%20Transport)
- **AT Open Data Portal**: [data-atgis.opendata.arcgis.com](https://data-atgis.opendata.arcgis.com)
- **AT GTFS / real-time feeds**: [dev-portal.at.govt.nz](https://dev-portal.at.govt.nz) — for live arrivals + schedule
- **AT Journey Planner** (consumer-facing): [at.govt.nz/bus-train-ferry/journey-planner](https://at.govt.nz/bus-train-ferry/journey-planner)

## Related

- [Auckland Council](auckland-council.md) — for AUP planning data (different agency)
- [Waka Kotahi / NZTA](nzta.md) — for state highway + driver licence data
- [Councils overview](councils.md) — the full council coverage model
- [Examples](../examples/index.md) — boundary mapping recipes
