# Data sources

eolas serves data from 22+ official New Zealand and international sources. Each is loaded directly from the agency's own API or published files, normalised to a consistent schema, refreshed on a schedule, and exposed through the same REST endpoint.

This section has a per-source guide for the most-queried agencies — covering what's in the catalogue, how often we refresh, the license, and quick-start code for each.

## NZ government statistical agencies

| Source                                                               | Datasets | Refresh           | Guide                                                                                                                         |
| -------------------------------------------------------------------- | -------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [Stats NZ](https://docs.eolas.nz/sources/statsnz/index.md)           | 415      | Weekly Wed AM NZT | Macro indicators, business demography, population, justice, productivity, **plus ~230 geospatial / census boundary datasets** |
| [RBNZ](https://docs.eolas.nz/sources/rbnz/index.md)                  | 33       | Weekly            | Interest rates, exchange rates, money supply, mortgages, BoP, financial-stability indicators                                  |
| [NZ Treasury](https://docs.eolas.nz/sources/treasury/index.md)       | 5        | Monthly           | Fiscal spending, revenue, debt, NZSF, GDP estimates                                                                           |
| [MBIE](https://docs.eolas.nz/sources/mbie/index.md)                  | 12       | Weekly            | Fuel prices, gas stats, rental bonds, GETS tender awards, science funding                                                     |
| [Waka Kotahi / NZTA](https://docs.eolas.nz/sources/nzta/index.md)    | 5        | Weekly            | CAS crashes, driver licences, EV charging, TMS daily traffic, traffic monitoring sites                                        |
| [Immigration NZ](https://docs.eolas.nz/sources/immigration/index.md) | 16       | Weekly            | RDA visa decisions (residence, visitor, work, student), RSE seasonal-worker stats                                             |

## International + comparative

| Source                                              | Datasets | Refresh | Guide                                                                                                                                      |
| --------------------------------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [OECD](https://docs.eolas.nz/sources/oecd/index.md) | 5        | Weekly  | NZ macro indicators on OECD's KEI dataflow — CPI, GDP, unemployment, interest rates (short + long), all comparable to other OECD economies |

## Geospatial

| Source                                                               | Datasets | Refresh | Guide                                                                                            |
| -------------------------------------------------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------ |
| [LINZ](https://docs.eolas.nz/sources/linz/index.md)                  | 106      | Weekly  | Parcels, addresses, road centrelines, suburbs, geodetic marks, place names, Antarctic + offshore |
| [Manaaki Whenua / LRIS](https://docs.eolas.nz/sources/lris/index.md) | 20       | Weekly  | Land cover (LCDB v6 + older vintages), NZ Land Use Map, Protected Areas Network                  |

Stats NZ also publishes ~230 census + boundary geospatial datasets — meshblocks, SA1/2/3, TLAs, regional councils, urban areas, wards across 2013 / 2018 / 2023 vintages. Those live in the [Stats NZ guide](https://docs.eolas.nz/sources/statsnz/#geospatial-boundaries-census).

## Council + regional

See the [Councils overview](https://docs.eolas.nz/sources/councils/index.md) for the full coverage model — how clusters work, what's common across district plans, hazards, mana whenua sites, and where the data comes from.

| Cluster                                                                         | Datasets | Refresh | Coverage                                                                                                    |
| ------------------------------------------------------------------------------- | -------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| [Auckland Council](https://docs.eolas.nz/sources/auckland-council/index.md)     | 20       | Weekly  | District Plan overlays — aircraft noise, heritage, ecology, hazards, water management                       |
| [Auckland Transport](https://docs.eolas.nz/sources/auckland-transport/index.md) | 10       | Weekly  | Bridges, bus / ferry / train routes, cycle network, park & ride                                             |
| [Bay of Plenty](https://docs.eolas.nz/sources/bay-of-plenty/index.md)           | 46       | Weekly  | BoPRC + Kawerau, Ōpōtiki, Rotorua, Tauranga, Western Bay councils                                           |
| [Canterbury / ECan](https://docs.eolas.nz/sources/canterbury/index.md)          | 85       | Weekly  | ECan + Ashburton, Christchurch, Hurunui, Selwyn, Timaru, Waimakariri, Waimate councils                      |
| [Co-Lab Waikato](https://docs.eolas.nz/sources/colab-waikato/index.md)          | 79       | Weekly  | Hamilton, Hauraki, Matamata-Piako, Otorohanga, Rotorua-Lakes, South Waikato, Taupō, Waikato, Waipa, Waitomo |
| [DOC](https://docs.eolas.nz/sources/doc/index.md)                               | 10       | Weekly  | Campsites, huts, marine reserves, tracks, walking experiences, public conservation land                     |
| [Hawke's Bay](https://docs.eolas.nz/sources/hawkes-bay/index.md)                | 33       | Weekly  | HBRC + CHBDC + Hastings councils                                                                            |
| [Manawatū-Whanganui](https://docs.eolas.nz/sources/manawatu-whanganui/index.md) | 46       | Weekly  | Horizons + Horowhenua, Manawatū, Palmerston North, Rangitīkei, Ruapehu, Tararua, Whanganui                  |
| [Napier + Whanganui](https://docs.eolas.nz/sources/napier-whanganui/index.md)   | 20       | Weekly  | NCC + WDC city-council layers                                                                               |
| [Northland](https://docs.eolas.nz/sources/northland/index.md)                   | 28       | Weekly  | NRC + Far North, Kaipara, Whangārei councils                                                                |
| [Otago](https://docs.eolas.nz/sources/otago/index.md)                           | 41       | Weekly  | ORC + Central Otago, Clutha, Dunedin, Queenstown-Lakes, Waitaki councils                                    |
| [Southland](https://docs.eolas.nz/sources/southland/index.md)                   | 48       | Weekly  | ES + Gore, Invercargill, Southland District councils                                                        |
| [Taranaki](https://docs.eolas.nz/sources/taranaki/index.md)                     | 33       | Weekly  | TRC + New Plymouth, South Taranaki, Stratford councils                                                      |
| [Gisborne / Top of South](https://docs.eolas.nz/sources/top-of-south/index.md)  | 45       | Weekly  | Gisborne, Marlborough, Nelson, Tasman councils                                                              |
| [Wellington](https://docs.eolas.nz/sources/wellington/index.md)                 | 76       | Weekly  | GWRC + Carterton, Hutt, Kāpiti, Masterton, Porirua, South Wairarapa, Upper Hutt, Wellington councils        |
| [West Coast](https://docs.eolas.nz/sources/west-coast/index.md)                 | 24       | Weekly  | WCRC + Buller, Grey, Westland councils (shared Te Tai o Poutini Plan)                                       |

## Other

| Source                                                                      | Datasets | Refresh   | Coverage                                                              |
| --------------------------------------------------------------------------- | -------- | --------- | --------------------------------------------------------------------- |
| [ACC](https://docs.eolas.nz/sources/acc/index.md)                           | 73       | Monthly   | Injury claims by activity (sport, work, vehicle, age cohort)          |
| [Charities Services](https://docs.eolas.nz/sources/charities/index.md)      | 6        | Monthly   | Charitable trust registry, financial returns                          |
| [Education Counts](https://docs.eolas.nz/sources/education-counts/index.md) | 38       | Quarterly | Schools, ECE, tertiary enrolments and outcomes                        |
| [MSD](https://docs.eolas.nz/sources/msd/index.md)                           | 12       | Monthly   | Benefit recipients, working-age caseload, corrections                 |
| [NZ Police / MoJ](https://docs.eolas.nz/sources/police-moj/index.md)        | 5        | Quarterly | Road policing offences, MoJ charges, criminal court data              |
| [PHARMAC](https://docs.eolas.nz/sources/pharmac/index.md)                   | 4        | Monthly   | Community + hospital medicines schedules with 14-year monthly history |
| [WorkSafe NZ](https://docs.eolas.nz/sources/worksafe/index.md)              | 8        | Monthly   | Workplace fatalities, notifiable injuries by sector                   |
| [EECA](https://docs.eolas.nz/sources/eeca/index.md)                         | 6        | Quarterly | EV charging infrastructure, EEUD energy end-use, regional heat demand |

## How sources work in eolas

Every source goes through the same pipeline: a per-source **Singer tap** pulls from the agency's API or published files, **target-iceberg** writes the result as an Iceberg table in S3, **AWS Glue** catalogues the schema, and **Snowflake** mirrors the table for Enterprise customers via a zero-copy share. The same data is served back through our REST API for everyone else.

The pipelines run on AWS Fargate via EventBridge schedules. Each table has metadata describing its source, license, last-refresh time, geometry type (where spatial), and replication mode (overwrite / append / SCD2). The clients surface these on every dataset call.

For specifics of any source not yet linked here — refresh time, license, sample queries — visit [eolas.nz/datasets](https://eolas.nz/datasets) and use the source filter.
