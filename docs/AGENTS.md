# AGENTS.md — eolas for coding agents

Everything an AI coding agent needs to use the eolas API correctly on the first try.
Human-oriented docs: [Getting started](quickstart.md).

## What eolas is

A read-only HTTP API serving cleaned, versioned New Zealand and OECD public data
(~1,500 datasets) as JSON, CSV, Arrow, or Parquet. One schema, one auth scheme,
one date format across every agency.

- **Base URL:** `https://api.eolas.fyi` — all data routes are under `/v1`
- **Auth:** `X-API-Key: vs_...` header on every `/v1` request
- **Override the host** with the `EOLAS_BASE_URL` env var (both clients honour it)

## Fastest correct path

Prefer the official clients over raw HTTP — they handle paging, retries, typed
columns, and the large-dataset routing rules below.

=== "Python"

    ```bash
    pip install eolas-data
    export EOLAS_API_KEY=vs_your_key
    ```

    ```python
    from eolas_data import Client
    client = Client()                                  # reads EOLAS_API_KEY

    client.search("unemployment")                      # find a dataset
    client.info("nz_unemployment")                     # schema + provenance
    df = client.get("nz_unemployment", start="2015-01-01")
    ```

=== "R"

    ```r
    remotes::install_github("phildonovan/eolas-r")
    ```

    ```r
    library(eolas)
    eolas_key("vs_your_key")

    eolas_search("unemployment")
    eolas_info("nz_unemployment")
    df <- eolas_get("nz_unemployment", start = "2015-01-01")
    ```

=== "curl"

    ```bash
    curl -H "X-API-Key: $EOLAS_API_KEY" \
      "https://api.eolas.fyi/v1/datasets/nz_unemployment/data?start=2015-01-01&limit=1000"
    ```

## Endpoints

| Route | Auth | Purpose |
|---|---|---|
| `GET /v1/datasets` | key | List every dataset with metadata |
| `GET /v1/datasets/{name}` | key | One dataset: schema, columns, provenance, snapshot id |
| `GET /v1/datasets/{name}/preview` | **none** | Up to 10 rows — cheap shape check |
| `GET /v1/datasets/{name}/data` | key | The rows |
| `GET /v1/datasets/{name}/changes` | key | Incremental changes since a watermark |
| `GET /v1/bulk/{namespace}/{name}` | key | Whole-dataset file download |
| `GET /health` | none | Liveness |

### `/data` query parameters

| Param | Default | Notes |
|---|---|---|
| `start`, `end` | – | `YYYY-MM-DD`, inclusive. No-ops if the dataset has no date axis (check `date_filter_column`). |
| `limit` | `100` | **`0` means "everything"** — see the guard below. |
| `format` | `json` | `json` \| `csv` \| `arrow` \| `parquet` |
| `dimensions` | – | Case-insensitive substring match across dimension columns |
| `geometry` | `true` | `false` omits `geometry_wkt` on spatial datasets — much smaller and faster |
| `envelope` | `false` | JSON only: wraps rows as `{"data_sources": [...], "data": [...]}` with licence metadata |

**Use `format=arrow` or `format=parquet` for anything large** — columnar and typed,
3–10× faster end-to-end into pandas/R than JSON, and no float/int coercion surprises.

## Rules that will otherwise cost you a retry

1. **The default is 100 rows, not the whole dataset.** Omitting `limit` silently
   truncates. Pass an explicit `limit`, or `limit=0` for everything.

2. **`limit=0` is rejected with HTTP 413** when the dataset has >100,000 rows *or*
   contains geometry *and* you passed no `start`/`end`. This is deliberate — use the
   bulk endpoint (`/v1/bulk/{namespace}/{name}`, or `client.download_bulk()` /
   `eolas_download_bulk()`) for whole-dataset pulls. Adding a date filter also clears
   the guard. **Bulk download requires Pro or Enterprise** — Free keys get `402`, and
   should page the live API with an explicit `limit` instead.

3. **Free tier caps at 50,000 rows per request and 10 requests per month.**
   Pro and Enterprise are unlimited on both. A truncated response sets
   `X-Eolas-Truncated: true` and `X-Plan-Row-Cap` — check them rather than assuming
   you got everything.

4. **Two-thirds of datasets carry a `geometry_wkt` column** (WKT, EPSG:4326, lon-lat)
   and it usually dwarfs the rest of the row. **Pass `geometry=false`** if you only
   need the attributes — the column is projected away at the storage layer, so it is
   never read or transferred, and the response sets `X-Eolas-Geometry-Omitted: true`.
   This also clears the 413 guard for small spatial tables.

5. **Dataset shape varies by upstream format.** Some series are long
   (`date, period, value`), others are wide (one column per series, e.g.
   `rbnz_b1_exchange_rates_monthly` has 21). Call `info()` before assuming a shape.

6. **Rate limits surface as `429`** with `X-RateLimit-*` headers. Back off; don't retry
   in a tight loop.

## Provenance — cite the source, not eolas

Most datasets are CC-BY and the credit must travel with the data. Every `/data`
response carries:

- `X-Eolas-Attribution` — the ready-made credit string; use this verbatim
- `X-Eolas-Source`, `X-Eolas-Licence`, `X-Eolas-Source-URL`, `X-Eolas-Namespace`

The same fields are on `info()` as `attribution_text`, `licence`, `source_url`.
`source_url_precision` tells you what `source_url` points at:

- `"dataset"` — addresses this dataset specifically, not just the agency. Note
  this means "more specific than the homepage", not "a tidy human-facing page":
  some are direct data endpoints (an OECD SDMX query, an `.xlsx`, an `.rda`).
  Good for reproducibility; check it before pasting into a reference list.
- `"source"` — only the publishing agency's landing page (that dataset isn't
  individually stamped yet); cite the agency, not the URL, as the dataset location
- `null` — no URL known

## Conventions you can rely on

- **Column names** are `snake_case` everywhere.
- **Dates** are ISO-8601 `YYYY-MM-DD` strings (not native date types).
- **Period codes**, where present, are in the `period` column: `2024-Q1`, `2024-03`,
  `2024`, `2023/24`. Wide tables typically have only `date`. Check `info()`.
- **Geometry** is always the `geometry_wkt` column: WKT, EPSG:4326, lon-lat order,
  `MULTI*` forms even for single rings.
- **Percentages** are proportions (`0.05`), not percents (`5`).
- **Booleans** are real booleans, never `"Y"`/`"N"`.

Full spec: [data conventions](https://github.com/phildonovan/eolas).

## Freshness

`info()` returns:

- `last_refreshed_at` — when the data itself last changed ("data as of")
- `refresh_cadence` — how often **eolas re-checks the source** (`daily`, `weekly`, …).
  This is the pipeline's cadence, **not** the frequency of the series itself.
- `row_count_at_last_refresh`, `current_snapshot_id`

Note the separate `freshness=` parameter on the **bulk** endpoint means something
different again: which snapshot tier you're entitled to (`monthly` or `current`).

## Errors

| Code | Meaning | Do this |
|---|---|---|
| `401` | Missing/invalid `X-API-Key` | Check the key; it starts with `vs_` |
| `402` | Bulk download on a Free key | Upgrade, or page `/data` with an explicit `limit` |
| `403` | Licence forbids bulk redistribution | Query `/data` instead; no plan unlocks it |
| `404` | No such dataset | `search()` for the right name — don't guess |
| `413` | Unbounded pull on a large/geo dataset | Use bulk, or add `start`/`end`/`limit` |
| `429` | Rate limited | Back off. Check `X-RateLimit-*` and `cf-ray` |

## Don't

- Don't scrape the website — the API serves the same data, faster and licensed.
- Don't hardcode `https://api.eolas.fyi`; read `EOLAS_BASE_URL` with that as default.
- Don't paginate manually — the clients stream; use `limit=0` or the bulk endpoint.
- Don't cache across snapshots without checking `current_snapshot_id`.
