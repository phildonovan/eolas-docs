# NZTA (Waka Kotahi) data via eolas

[Waka Kotahi NZ Transport Agency](https://www.nzta.govt.nz) (NZTA) is the agency responsible for the state highway network, vehicle and driver licensing, road safety, and the EV charging rollout. eolas serves **5 datasets** from NZTA — small in count but heavy in research value: crash records since 2000, the entire licence-holder population, and traffic counts at every state highway telemetry site.

If you're doing road-safety research, transport-policy analysis, EV-infrastructure planning, or modelling traffic flows — NZTA is the source.

---

## What's in the catalogue

| Dataset | Description |
|---|---|
| `nzta_cas_crashes` | All recorded NZ road crashes since 2000 (~900k records). Includes severity (fatal / serious / minor / non-injury), location, road conditions, vehicle types, intoxication flags. The canonical road-safety dataset. |
| `nzta_driver_licences` | Count of NZ driver licence holders by region, class (car, motorcycle, heavy combination, etc.), and stage (learner / restricted / full). |
| `nzta_ev_charging` | All public EV charging stations in NZ — operator, address, connector types, plug count. |
| `nzta_tms_daily_traffic` | Daily vehicle counts at state highway Telemetry Monitoring Sites since 2018 (~7.3M records), broken down by vehicle weight class. The granular traffic-flow source. |
| `nzta_traffic_monitoring_sites` | Annual Average Daily Traffic (AADT) at all state highway monitoring sites, with five-year trend snapshots. The summary version of TMS daily traffic. |

---

## Refresh schedule

Weekly, Wednesday morning NZ time.

- CAS crashes update as new investigations close — typically a 1-3 month lag between an incident and its appearance in the published data.
- Driver licences and EV charging refresh from the NZTA Open Data Portal.
- TMS daily traffic publishes T+1 (next day) at the source — our weekly refresh catches up to ~5-7 days of fresh data each Wednesday.

```python
meta = client.info("nzta_cas_crashes")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All NZTA data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)** via the [NZTA Open Data Portal](https://opendata-nzta.opendata.arcgis.com). Commercial use is fine; attribution required.

Recommended attribution: *"Source: Waka Kotahi NZ Transport Agency, served via eolas (eolas.fyi). CC-BY 4.0."*

A privacy note for `nzta_cas_crashes`: NZTA has already aggregated/redacted personal information (no driver names, no plate numbers). What you get is incident-level data suitable for analysis.

---

## Common patterns

### Fatal-crash trend by region

=== "Python"

    ```python
    import matplotlib.pyplot as plt

    crashes = client.nzta("nzta_cas_crashes", start="2015-01-01")
    fatal = crashes[crashes["crash_severity"] == "Fatal Crash"]
    by_year = fatal.groupby(["crash_year", "region"])["objectid"].count().unstack()
    by_year.plot(figsize=(10, 6), title="Fatal crashes by region")
    plt.show()
    ```

=== "R"

    ```r
    library(dplyr)
    library(ggplot2)

    crashes <- eolas_get_nzta("nzta_cas_crashes", start = "2015-01-01")
    fatal <- crashes |>
      filter(crash_severity == "Fatal Crash") |>
      count(crash_year, region)

    ggplot(fatal, aes(crash_year, n, colour = region)) +
      geom_line() +
      labs(title = "Fatal crashes by region", y = "Count")
    ```

### State highway traffic over time

```python
tms = client.nzta("nzta_tms_daily_traffic", start="2020-01-01")
# tms columns: site_ref, date, light_volume, heavy_volume, total_volume

# State Highway 1 around Wellington — one site code
sh1_well = tms[tms["site_ref"] == "01N00251"]
sh1_well.plot(x="date", y="total_volume", title="SH1 Ngauranga daily traffic")
```

### EV charging coverage by territorial authority

```python
import geopandas as gpd

ev = client.nzta("nzta_ev_charging", as_sf=True)
# Join to TLA boundaries (LINZ) for coverage analysis
ta = client.linz("nz_territorial_authorities", as_sf=True)
ev_by_ta = gpd.sjoin(ev, ta, how="inner", predicate="within")
coverage = ev_by_ta.groupby("ta_name").size().sort_values(ascending=False).head(15)
print(coverage)
```

### Active monitoring sites with rising AADT

```python
mon = client.nzta("nzta_traffic_monitoring_sites")
# Five-year growth >= 20%
growing = mon[mon["aadt_5yr_pct_change"] >= 20].sort_values("aadt_5yr_pct_change", ascending=False)
print(growing.head(20))
```

---

## Source-specific notes

- **CAS reporting lag**: a fatal crash that happens today won't appear in the CAS feed for ~30-90 days while the police investigation closes. For up-to-the-minute road-toll stats, use NZTA's [Road Toll dashboard](https://www.nzta.govt.nz/safety/safety-resources/road-safety-information-and-tools/road-deaths). For longitudinal research, CAS is authoritative.
- **TMS site coverage**: ~600 telemetry sites covering the State Highway network only. Council-managed roads aren't in TMS — for those you'd need to ask each council (most don't publish equivalent open data).
- **Light vs heavy split**: TMS volumes split at ~3.5t GVM. "Heavy" here means trucks + buses; "light" means cars + light commercials.
- **EV charging is operator-published**: NZTA aggregates from operator submissions. Newly-opened stations may take 1-2 weeks to appear. For the absolute latest, [PlugShare](https://www.plugshare.com) and operator apps are faster — but NZTA is canonical.
- **Driver licences are stock not flow**: this is a snapshot of current licence holders, not the count of licences issued. For new-licence flow you'd need the (smaller) test-pass data, which isn't currently in eolas.
- **Geometry**: `nzta_cas_crashes`, `nzta_ev_charging`, `nzta_tms_daily_traffic`, and `nzta_traffic_monitoring_sites` all have a `geometry_wkt` column. Use `as_sf=True` to get a GeoDataFrame in Python.

---

## Where to find more

- **NZTA datasets on eolas**: [eolas.fyi/datasets?source=Waka+Kotahi](https://eolas.fyi/datasets?source=Waka%20Kotahi)
- **NZTA Open Data Portal**: [opendata-nzta.opendata.arcgis.com](https://opendata-nzta.opendata.arcgis.com)
- **Road Toll dashboard**: [www.nzta.govt.nz/safety](https://www.nzta.govt.nz/safety/safety-resources/road-safety-information-and-tools/road-deaths)
- **TMS site map** (visual): [www.nzta.govt.nz/traffic-and-travel-information](https://www.nzta.govt.nz/traffic-and-travel-information/traffic-volumes)

## Related

- [LINZ source guide](linz.md) — for road centrelines + addresses that geocode against TMS sites
- [Examples](../examples/index.md) — boundary mapping recipes
