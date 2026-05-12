# GeoNet data via eolas

[GeoNet](https://www.geonet.org.nz) is the joint geological hazard monitoring programme run by [GNS Science](https://www.gns.cri.nz), the Earthquake Commission (Toka Tū Ake EQC), and Toitū Te Whenua LINZ. It operates the seismic + GNSS + volcano monitoring networks. eolas serves **3 datasets** from GeoNet — the canonical reference for recent quakes and current volcanic alert levels.

If you're doing seismic-risk modelling, volcanic-hazard work, or building real-time earthquake-aware applications — GeoNet is the source.

For *historical* major earthquakes + fault locations, use the council-published earthquake-hazard layers (e.g. [ECan / Canterbury](canterbury.md)'s `ecan_earthquake_faults_2024`).

---

## What's in the catalogue

| Dataset | Description |
|---|---|
| `geonet_quakes_recent` | Current rolling window of NZ earthquakes with Modified Mercalli Intensity ≥3 — magnitude, depth, location, intensity, origin time. |
| `geonet_strong_motion_sensors` | Reference data for strong-motion sensor stations across NZ (network code, station, location). |
| `geonet_volcanic_alert_levels` | Current alert level (Green / Yellow / Orange / Red), activity description, and hazards for each monitored NZ volcano. |

---

## Refresh schedule

Weekly. For *real-time* earthquake feeds, use GeoNet's own [WFS/JSON APIs](https://api.geonet.org.nz) — those update within seconds of an event. Our weekly snapshot is suited to research / dashboard use cases, not emergency-response.

```python
meta = client.info("geonet_quakes_recent")
meta["last_refreshed_at"]
```

---

## License

All GeoNet data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: GeoNet (GNS Science / Toka Tū Ake EQC / LINZ), served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### Recent quake magnitude distribution

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    q = client.geonet("geonet_quakes_recent")
    q["magnitude"].hist(bins=30)
    plt.title("Recent NZ earthquake magnitudes (M ≥ 3)")
    plt.xlabel("Magnitude (ML)")
    plt.show()
    ```

=== "R"

    ```r
    library(ggplot2)
    q <- eolas_get_geonet("geonet_quakes_recent")
    ggplot(q, aes(magnitude)) + geom_histogram(bins = 30) +
      labs(title = "Recent NZ earthquakes", x = "Magnitude (ML)")
    ```

### Volcanic alert dashboard

```python
v = client.geonet("geonet_volcanic_alert_levels")
print(v[["volcano", "alert_level", "activity_description"]])
```

### Strong-motion network map

```python
import geopandas as gpd
sensors = client.geonet("geonet_strong_motion_sensors", as_sf=True)
print(f"Strong-motion sensor stations: {len(sensors)}")
sensors.plot(figsize=(8, 10), markersize=5)
```

---

## Source-specific notes

- **Recent ≠ historical**: `geonet_quakes_recent` is a rolling window (typically last ~30 days). For historical quake catalogues, use GeoNet's [data archives](https://www.geonet.org.nz/data/types/quake_search).
- **Intensity vs magnitude**: Modified Mercalli (MMI) measures perceived shaking at a location; magnitude measures the energy released at the source. A M6 quake 100km offshore might produce MMI 4 onshore; a M4 directly underneath could produce MMI 5.
- **Volcanic alert levels**: 5-level scale (0=no unrest through 5=major eruption). Each volcano has its own characteristic activity baseline. Whakaari/White Island has been at Level 2 since the 2019 eruption; Tongariro/Ruapehu fluctuate between 0-2 routinely.
- **Use the live API for real-time apps**: GeoNet publishes earthquake events within seconds via [api.geonet.org.nz](https://api.geonet.org.nz). Our weekly refresh isn't appropriate for emergency-response use cases.
- **Coverage**: GeoNet's seismic network is densest in populated areas + active volcanic regions. Strong-motion sensors are biased toward critical infrastructure + dam sites.

---

## Where to find more

- **GeoNet datasets on eolas**: [eolas.fyi/datasets?source=GeoNet](https://eolas.fyi/datasets?source=GeoNet)
- **GeoNet portal**: [www.geonet.org.nz](https://www.geonet.org.nz)
- **Real-time APIs**: [api.geonet.org.nz](https://api.geonet.org.nz)
- **Historical quake search**: [www.geonet.org.nz/quakes](https://www.geonet.org.nz/quakes)

## Related

- [Canterbury / ECan source guide](canterbury.md) — for historical earthquake-fault hazards
- [Examples](../examples/index.md) — worked code recipes
