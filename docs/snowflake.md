# Snowflake share

**Enterprise plan.** eolas publishes the entire warehouse to your Snowflake account as a
[Snowflake secure data share](https://docs.snowflake.com/en/user-guide/data-sharing-intro) —
zero-copy, no ETL on your side. You mount one database and query ~1,500 always-fresh NZ + OECD
datasets as native Iceberg tables, with eolas refreshing the underlying data on each source's
cadence. Your compute, our data.

This page is the end-to-end lifecycle: prerequisites → request → mount → query → refresh →
offboarding.

---

## 1. Prerequisites

| Requirement | Detail |
|---|---|
| **eolas plan** | Enterprise. [Talk to us](mailto:phil@eolas.fyi?subject=Snowflake%20share) to enable it. |
| **Cloud + region** | Your Snowflake account must be on **AWS `ap-southeast-2` (Sydney)** — the share is region- and cloud-local. |
| **Role** | An `ACCOUNTADMIN` (or a role with `IMPORT SHARE` + `CREATE DATABASE`) to mount the share. |

!!! note "Not on AWS Sydney?"
    Snowflake secure shares only work directly when provider and consumer are in the **same
    cloud + region**. If your account is on Azure, GCP, or another AWS region, we provision a
    **replicated reader path** instead (a small surcharge covers the cross-region replication).
    Tell us your account's cloud + region when you get in touch and we'll confirm the approach.

---

## 2. Request the share

Email **phil@eolas.fyi** with:

1. Your **Snowflake account identifier** — run this in your account and paste the result:
   ```sql
   SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME() AS account_locator,
          CURRENT_REGION() AS region;
   ```
2. Your **organisation name** (for the access record).

We add your account to the share and confirm — typically **within one business day**. There is
nothing to install and no data egress on your side.

---

## 3. Mount the share

Once we've confirmed your account is added, mount it (one-time):

```sql
CREATE DATABASE eolas FROM SHARE MRWTYQY-WZ79363.vs_warehouse_share;
```

`eolas` is just the local database name — call it whatever suits your conventions. That's the
whole setup; the data is queryable immediately.

---

## 4. What's in the share (layout)

```
eolas  (database)
 └── <namespace>  (schema, one per data source)
      └── <dataset>  (Iceberg table)
```

Each **schema is a source namespace** and each **table is a dataset** — the same names you see
in the [dataset catalogue](https://eolas.fyi/datasets) and the API. Discover everything from SQL:

```sql
-- every source namespace
SHOW SCHEMAS IN DATABASE eolas;

-- every dataset in a namespace
SHOW TABLES IN SCHEMA eolas.rbnz;

-- column names + types for one dataset
DESCRIBE TABLE eolas.rbnz.rbnz_b2_wholesale_rates_daily;
```

The 35 namespaces: `rbnz`, `stats_nz`, `treasury`, `oecd`, `linz`, `statsnz_geo`, `lris`, `nzta`,
`doc`, `mbie`, `msd`, `acc`, `police`, `edcounts`, `worksafe`, `charities`, `immigration`,
`pharmac`, `eeca`, `geonet`, plus the regional-council namespaces (`akl_council`, `akl_transport`,
`bay_of_plenty`, `colab_waikato`, `ecan_canterbury`, `hawkes_bay`, `manawatu_whanganui`,
`napier_whanganui`, `northland`, `otago`, `southland`, `taranaki`, `top_of_south`, `wellington`,
`west_coast`).

---

## 5. Query

Native SQL — no special syntax:

```sql
-- NZ Official Cash Rate, last 12 observations
SELECT date, cash_rate_official_cash_rate_ocr
FROM eolas.rbnz.rbnz_b2_wholesale_rates_daily
ORDER BY date DESC
LIMIT 12;
```

Spatial datasets carry a `geometry_wkt` column (WGS84 WKT). Parse it with Snowflake's geospatial
functions:

```sql
SELECT name, TO_GEOGRAPHY(geometry_wkt) AS geom
FROM eolas.linz.nz_parcels
LIMIT 100;
```

dbt users: point a source at the `eolas` database and reference tables as
`{{ source('rbnz', 'rbnz_b2_wholesale_rates_daily') }}`.

---

## 6. Freshness

The share is **live** — there is no copy step, so the moment eolas refreshes a dataset it's
visible in your account. Each dataset refreshes on its source's cadence (daily for FX/rates,
monthly/quarterly for most official statistics, etc.); the per-dataset cadence and
"data as of" are on each [dataset page](https://eolas.fyi/datasets) and in the API metadata
(`refresh_cadence`, `last_refreshed_at`). New datasets we add appear in the share automatically.

!!! info "Licensing"
    Shared datasets carry their source licence and required attribution in the dataset metadata.
    Most NZ government data is CC-BY 4.0 (attribution required). A small number of sources are
    excluded from the share for licensing reasons — those aren't granted and won't appear.

---

## 7. Offboarding

To stop, simply `DROP DATABASE eolas;` in your account — nothing of ours remains, since the share
is zero-copy. Tell us and we'll remove your account from the share access list.

---

Questions, a non-Sydney account, or a custom dataset request?
**[phil@eolas.fyi](mailto:phil@eolas.fyi?subject=Snowflake%20share)**.
