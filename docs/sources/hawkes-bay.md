# Hawke's Bay Councils data via eolas

The Hawke's Bay region covers ~180,000 people. eolas serves **33 datasets** from [Hawke's Bay Regional Council](https://www.hbrc.govt.nz) (HBRC) and Central Hawke's Bay District Council (CHBDC), with comprehensive post-Cyclone Gabrielle hazard data. Napier City + Hastings District publish via separate portals — Napier is in the [Napier + Whanganui cluster](napier-whanganui.md).

If you're doing Hawke's Bay property research, cyclone-resilience analysis, or agricultural land-use work — this is the source.

---

## What's in the catalogue

| Council | Code | Datasets | Highlights |
|---|---|---|---|
| HBRC | hbrc | 14 | Coastal erosion (66/100/150yr scenarios), liquefaction, river flood scenarios, water-management areas |
| Central Hawke's Bay District (CHBDC) | chbdc | 13 | Full DP suite + post-Gabrielle cyclone-affected properties + flood scenarios |
| Hastings District (HDC) | hdc | 6 | DP zones + designations |

### Standout datasets

- `chbdc_cyclone_affected_properties` — post-Cyclone Gabrielle property impacts (Feb 2023). Critical for property + insurance research.
- `hbrc_coastal_erosion_likely_66`, `hbrc_coastal_erosion_likely_66`, `hbrc_coastal_erosion_possible_33` — multi-horizon coastal erosion scenarios
- `hbrc_chb_hdc_wdc_liquefaction_severity` — liquefaction severity for Central HB + Hastings + Wairoa (combined regional product)
- `chbdc_haz_flood_full`, `chbdc_haz_flood_risk_areas` — Central HB flood hazards
- `chbdc_haz_tsunami_inundation` — tsunami inundation modelling (Pacific exposure)

Browse: [eolas.fyi/datasets?source=Hawke%27s+Bay+Councils](https://eolas.fyi/datasets?source=Hawke%27s%20Bay%20Councils).

---

## Refresh schedule

Weekly, Wednesday morning NZ time. HBRC + CHBDC use ArcGIS portals.

---

## License

All HB council data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

---

## Common patterns

### Post-Gabrielle property impact

```python
affected = client.hawkes_bay("chbdc_cyclone_affected_properties", as_sf=True)
# affected has impact_category column
print(affected["impact_category"].value_counts())
```

### Multi-horizon coastal erosion

```python
import geopandas as gpd

scenarios = {
    "66yr":  client.hawkes_bay("hbrc_coastal_erosion_likely_66", as_sf=True),
    "100yr": client.hawkes_bay("hbrc_coastal_erosion_likely_66", as_sf=True),
    "150yr": client.hawkes_bay("hbrc_coastal_erosion_possible_33", as_sf=True),
}
for label, layer in scenarios.items():
    area_km2 = layer.to_crs("EPSG:2193").area.sum() / 1e6
    print(f"{label} likely-erosion area: {area_km2:.1f} km²")
```

---

## Source-specific notes

- **Cyclone Gabrielle context**: Hawke's Bay was the worst-affected region in February 2023. `chbdc_cyclone_affected_properties` is a CHBDC-specific dataset; equivalent layers for Hastings + Napier + Wairoa exist on their own portals but aren't all in eolas yet.
- **Multi-horizon coastal-erosion modelling**: HBRC publishes 66yr / 100yr / 150yr scenarios — useful for forward-looking property + insurance work. Don't conflate with NIWA's sea-level-rise projections (different methodology).
- **Hastings + Napier**: Hastings publishes some data here (`hdc_*`) but more via its own portal. Napier is in the [Napier + Whanganui cluster](napier-whanganui.md) because of how its data is published.
- **Cross-cluster shared product**: `hbrc_chb_hdc_wdc_liquefaction_severity` is a joint product covering Central HB + Hastings + Wairoa — useful regional view.

---

## Where to find more

- **HB datasets on eolas**: [eolas.fyi/datasets?source=Hawke%27s+Bay+Councils](https://eolas.fyi/datasets?source=Hawke%27s%20Bay%20Councils)
- **HBRC**: [www.hbrc.govt.nz](https://www.hbrc.govt.nz)
- **CHBDC**: [www.chbdc.govt.nz](https://www.chbdc.govt.nz)

## Related

- [Councils overview](councils.md) | [Napier + Whanganui guide](napier-whanganui.md) | [Examples](../examples/index.md)
