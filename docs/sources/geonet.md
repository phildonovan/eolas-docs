# GeoNet

On 2026-10-04 eolas stopped serving the three GeoNet tables (`geonet_quakes_recent`, `geonet_volcanic_alert_levels`, `geonet_strong_motion_sensors`). They were a rolling status feed.

The tap that fetches them is still in the eolas repo at `taps/tap-geonet`. GeoNet publishes the live data itself:

- Live API: [api.geonet.org.nz](https://api.geonet.org.nz)
- Quake search: [geonet.org.nz/quakes](https://www.geonet.org.nz/quakes)
