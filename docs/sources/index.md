# Data sources

eolas serves data from 22+ official New Zealand and international sources. Each is loaded directly from the agency's own API or published files, normalised to a consistent schema, refreshed on a schedule, and exposed through the same REST endpoint.

This section has a per-source guide for the most-queried agencies — covering what's in the catalogue, how often we refresh, the license, and quick-start code for each.

## NZ government statistical agencies

| Source | Datasets | Refresh | Guide |
|---|---|---|---|
| [Stats NZ](statsnz.md) | 415 | Weekly Wed AM NZT | Macro indicators, business demography, population, justice, productivity, **plus ~230 geospatial / census boundary datasets** |
| [RBNZ](rbnz.md) | 33 | Weekly | Interest rates, exchange rates, money supply, mortgages, BoP, financial-stability indicators |
| [NZ Treasury](treasury.md) | 5 | Monthly | Fiscal spending, revenue, debt, NZSF, GDP estimates |
| [MBIE](mbie.md) | 12 | Weekly | Fuel prices, gas stats, rental bonds, GETS tender awards, science funding |
| [Waka Kotahi / NZTA](nzta.md) | 5 | Weekly | CAS crashes, driver licences, EV charging, TMS daily traffic, traffic monitoring sites |
| [Immigration NZ](immigration.md) | 16 | Weekly | RDA visa decisions (residence, visitor, work, student), RSE seasonal-worker stats |

## International + comparative

| Source | Datasets | Refresh | Guide |
|---|---|---|---|
| [OECD](oecd.md) | 5 | Weekly | NZ macro indicators on OECD's KEI dataflow — CPI, GDP, unemployment, interest rates (short + long), all comparable to other OECD economies |

## Geospatial

| Source | Datasets | Refresh | Guide |
|---|---|---|---|
| [LINZ](linz.md) | 106 | Weekly | Parcels, addresses, road centrelines, suburbs, geodetic marks, place names, Antarctic + offshore |
| [Manaaki Whenua / LRIS](lris.md) | 20 | Weekly | Land cover (LCDB v6 + older vintages), NZ Land Use Map, Protected Areas Network |

Stats NZ also publishes ~230 census + boundary geospatial datasets — meshblocks, SA1/2/3, TLAs, regional councils, urban areas, wards across 2013 / 2018 / 2023 vintages. Those live in the [Stats NZ guide](statsnz.md#geospatial-boundaries-census).

## Council + regional

See the [Councils overview](councils.md) for the full coverage model — how clusters work, what's common across district plans, hazards, mana whenua sites, and where the data comes from.

| Cluster | Datasets | Refresh | Coverage |
|---|---|---|---|
| [Auckland Council](auckland-council.md) | 20 | Weekly | District Plan overlays — aircraft noise, heritage, ecology, hazards, water management |
| [Auckland Transport](auckland-transport.md) | 10 | Weekly | Bridges, bus / ferry / train routes, cycle network, park & ride |
| [Bay of Plenty](bay-of-plenty.md) | 46 | Weekly | BoPRC + Kawerau, Ōpōtiki, Rotorua, Tauranga, Western Bay councils |
| [Canterbury / ECan](canterbury.md) | 85 | Weekly | ECan + Ashburton, Christchurch, Hurunui, Selwyn, Timaru, Waimakariri, Waimate councils |
| [Co-Lab Waikato](colab-waikato.md) | 79 | Weekly | Hamilton, Hauraki, Matamata-Piako, Otorohanga, Rotorua-Lakes, South Waikato, Taupō, Waikato, Waipa, Waitomo |
| [DOC](doc.md) | 10 | Weekly | Campsites, huts, marine reserves, tracks, walking experiences, public conservation land |
| GeoNet | 3 | Weekly | Recent quakes, strong-motion sensors, volcanic alert levels |
| [Hawke's Bay](hawkes-bay.md) | 33 | Weekly | HBRC + CHBDC + Hastings councils |
| [Manawatū-Whanganui](manawatu-whanganui.md) | 46 | Weekly | Horizons + Horowhenua, Manawatū, Palmerston North, Rangitīkei, Ruapehu, Tararua, Whanganui |
| [Napier + Whanganui](napier-whanganui.md) | 20 | Weekly | NCC + WDC city-council layers |
| [Northland](northland.md) | 28 | Weekly | NRC + Far North, Kaipara, Whangārei councils |
| [Otago](otago.md) | 41 | Weekly | ORC + Central Otago, Clutha, Dunedin, Queenstown-Lakes, Waitaki councils |
| [Southland](southland.md) | 48 | Weekly | ES + Gore, Invercargill, Southland District councils |
| [Taranaki](taranaki.md) | 33 | Weekly | TRC + New Plymouth, South Taranaki, Stratford councils |
| [Gisborne / Top of South](top-of-south.md) | 45 | Weekly | Gisborne, Marlborough, Nelson, Tasman councils |
| [Wellington](wellington.md) | 76 | Weekly | GWRC + Carterton, Hutt, Kāpiti, Masterton, Porirua, South Wairarapa, Upper Hutt, Wellington councils |
| [West Coast](west-coast.md) | 24 | Weekly | WCRC + Buller, Grey, Westland councils (shared Te Tai o Poutini Plan) |

## Other

| Source | Datasets | Refresh | Coverage |
|---|---|---|---|
| ACC | 73 | Monthly | Injury claims by activity (sport, work, vehicle, age cohort) |
| Charities Services | 6 | Monthly | Charitable trust registry, financial returns |
| Education Counts | 38 | Quarterly | Schools, ECE, tertiary enrolments and outcomes |
| MSD | 12 | Monthly | Benefit recipients, working-age caseload, corrections |
| NZ Police / MoJ | 5 | Quarterly | Road policing offences, MoJ charges, criminal court data |
| WorkSafe NZ | 8 | Monthly | Workplace fatalities, notifiable injuries by sector |
| EECA | (varies) | Quarterly | Energy use surveys, efficiency programmes |

## How sources work in eolas

Every source goes through the same pipeline: a per-source **Singer tap** pulls from the agency's API or published files, **target-iceberg** writes the result as an Iceberg table in S3, **AWS Glue** catalogues the schema, and **Snowflake** mirrors the table for Enterprise customers via a zero-copy share. The same data is served back through our REST API for everyone else.

The pipelines run on AWS Fargate via EventBridge schedules. Each table has metadata describing its source, license, last-refresh time, geometry type (where spatial), and replication mode (overwrite / append / SCD2). The clients surface these on every dataset call.

For specifics of any source not yet linked here — refresh time, license, sample queries — visit [eolas.fyi/datasets](https://eolas.fyi/datasets) and use the source filter.
