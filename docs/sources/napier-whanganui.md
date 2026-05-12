# Napier + Whanganui Councils data via eolas

This cluster covers two unrelated city/district councils that happen to publish via similar portals: **Napier City Council** (Hawke's Bay, ~67,000 people) and **Whanganui District Council** (Manawatū-Whanganui, ~50,000 people). eolas serves **20 datasets** across both.

Why grouped? Both publish via the WhanganuiData portal pattern, sharing data-pipeline plumbing. They have no geographic or political relationship.

If you're doing Napier or Whanganui property research, urban-planning analysis, or coastal-region work — this is the source.

---

## What's in the catalogue

### Whanganui District (WDC, wgnui) — 11 datasets

| Theme | Datasets |
|---|---|
| Heritage | `wgnui_heritage_buildings`, `wgnui_heritage_areas` |
| Cemeteries | `wgnui_aramoho_cemetery` |
| Airport | `wgnui_airport_noise_overlay`, `wgnui_airport_outer_control` |
| Alcohol bans | `wgnui_alcohol_ban_central_city`, `wgnui_alcohol_ban_kai_iwi` |
| Historic aerial | `wgnui_aerial_index_1968` (1968 aerial photo coverage) |

### Napier City Council — 9 datasets

| Theme | Datasets |
|---|---|
| Cadastral | `napier_parcels`, `napier_address_points`, `napier_road_centrelines` |
| Heritage | `napier_heritage_buildings`, `napier_heritage_areas` |
| District plan | `napier_dp_precincts` |
| Council infrastructure | `napier_council_buildings`, `napier_cemetery_plots`, `napier_building_footprints_2020` |

Browse: [eolas.fyi/datasets?source=Napier+%2B+Whanganui](https://eolas.fyi/datasets?source=Napier%20%2B%20Whanganui).

---

## Refresh schedule

Weekly, Wednesday morning NZ time.

---

## License

All cluster data is **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**.

---

## Common patterns

### Napier heritage walk

```python
import geopandas as gpd
heritage = client.napier_whanganui("napier_heritage_buildings", as_sf=True)
print(f"Napier heritage buildings: {len(heritage)}")
# Famous for Art Deco — most listings are 1930s reconstruction post-1931 earthquake
print(heritage[heritage["era"] == "Art Deco"].head(10))
```

### Whanganui historic 1968 aerial coverage

```python
aerial = client.napier_whanganui("wgnui_aerial_index_1968", as_sf=True)
# Index polygons + photo IDs — useful for historic-property research
print(aerial.head())
```

---

## Source-specific notes

- **Napier is Art Deco**: the 1931 Hawke's Bay earthquake destroyed central Napier, leading to rapid reconstruction in Art Deco style. The heritage-buildings layer is heavily 1930s — a key data product for the tourism + heritage sector.
- **Whanganui 1968 aerial**: an unusual offering — most councils don't publish historic aerial indexes. Useful for historical-property research.
- **Two unrelated councils, one cluster**: don't infer a relationship from the grouping. Both publish to similar portal infrastructure, which is why they pipeline together.
- **Napier also publishes other layers via the HBRC cluster**: for regional-scale data (coastal erosion, liquefaction), see [Hawke's Bay Councils](hawkes-bay.md).
- **Whanganui regional layers**: for regional-scale data, see [Manawatū-Whanganui Councils](manawatu-whanganui.md) (Horizons + the wider region).

---

## Where to find more

- **Cluster datasets on eolas**: [eolas.fyi/datasets?source=Napier+%2B+Whanganui](https://eolas.fyi/datasets?source=Napier%20%2B%20Whanganui)
- **Napier City**: [www.napier.govt.nz](https://www.napier.govt.nz)
- **Whanganui District**: [www.whanganui.govt.nz](https://www.whanganui.govt.nz)

## Related

- [Councils overview](councils.md) | [Hawke's Bay Councils](hawkes-bay.md) | [Manawatū-Whanganui](manawatu-whanganui.md) | [Examples](../examples/index.md)
