# Enterprise service level agreement

This page summarises the written SLA offered to **Enterprise** customers. Free and Pro plans are best-effort — see [eolas.fyi/terms](https://eolas.fyi/terms).

## API uptime

| Commitment | Detail |
|------------|--------|
| **Target** | 99.5% monthly uptime on the public API surface (`api.eolas.fyi`) |
| **Measurement** | External synthetic checks against `/health` every 3 minutes, plus internal subsystem checks on `/health/full` |
| **Exclusions** | Scheduled maintenance (announced ≥ 48 hours ahead), customer-side network issues, force majeure, upstream agency outages that do not reflect eolas infrastructure failure |

If monthly uptime falls below 99.5%, Enterprise customers may request a service credit (typically 10% of that month's fee per full 0.5% below target, capped at 30%). Credits are applied to the next invoice — not cash refunds.

## Data freshness

eolas maintains automated ETL pipelines for every live source. After each successful run we write a **pipeline heartbeat** to durable storage; the [status page](https://eolas.fyi/status) shows the last successful run per source.

| Cadence (typical) | Examples | Freshness commitment |
|-------------------|----------|----------------------|
| Daily | RBNZ, OECD | Successful check within **2×** the declared cadence |
| Weekly | Stats NZ, LINZ, most councils | Successful check within **2×** the declared cadence |
| Monthly / quarterly | Treasury, some MBIE series | Successful check within **2×** the declared cadence |
| Static / load-once | Some boundary layers | No refresh commitment — labelled `static` in dataset metadata |

A **successful check** means the pipeline ran to completion and verified upstream availability, even when the change-gate skipped a heavy re-download because data was unchanged. This is stricter than "data row changed" and matches what the heartbeat records.

Per-dataset `refresh_cadence` is exposed in API metadata and the Snowflake share. Enterprise contracts may add source-specific schedules or custom datasets.

## Support response

| Severity | Definition | Initial response |
|----------|------------|------------------|
| **P1** | API unavailable or widespread data access failure | 4 business hours |
| **P2** | Degraded performance, single-source freshness breach, incorrect values | 1 business day |
| **P3** | Questions, feature requests, non-urgent data issues | 3 business days |

Business hours: Mon–Fri, 09:00–17:00 NZST, excluding NZ public holidays. P1 contact: the dedicated support channel agreed in your order form.

## Observability

- **Live status:** [eolas.fyi/status](https://eolas.fyi/status) — subsystem health and per-source pipeline freshness (refreshes every minute).
- **Changelog:** [eolas.fyi/data/changelog](https://eolas.fyi/data/changelog) — dataset-level ingest events.
- **Security posture:** [eolas.fyi/security](https://eolas.fyi/security) — residency, subprocessors, breach notification.

## Contract

Enterprise SLAs are incorporated into the signed order form or MSA. This page is a plain-language summary; the contract prevails if anything differs.

For SLA-backed access, [contact us](https://eolas.fyi/contact).