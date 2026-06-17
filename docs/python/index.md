# Python client

The `eolas-data` Python package provides a `Client` class that wraps the eolas REST API and returns **`Dataset` objects** — pandas DataFrames with source metadata.

## Installation

```bash
pip install eolas-data
```

Optional extras:

```bash
pip install eolas-data[polars]      # polars output support
pip install matplotlib              # for plotting
```

Requires Python 3.10+ and pandas 1.5+.

## Initialisation

```python
from eolas_data import Client

# Pass key directly
client = Client("your_eolas_key")

# Read from EOLAS_API_KEY environment variable
client = Client()

# With in-memory cache (great for notebooks)
client = Client("your_eolas_key", cache=True)
```

## Source-specific helpers

The recommended way to fetch data — the source is encoded in the method name, making code self-documenting and autocomplete-friendly:

```python
df  = client.statsnz("nz_cpi", start="2020-01-01")   # Stats NZ
df  = client.oecd("nz_gdp_growth")                    # OECD
df  = client.rbnz("rbnz_b2_wholesale_rates_monthly")  # RBNZ
df  = client.treasury("treasury_fiscal_spending")     # NZ Treasury
gdf = client.linz("nz_parcels")  # LINZ (~3M rows — auto-bulks in seconds, no limit needed
```

Source-specific helpers call `client.get()` internally and inherit smart routing: large and geospatial datasets auto-route through the cache+sync path, so `client.linz("nz_parcels")` now returns a GeoDataFrame in seconds — not 15 minutes. The first call emits a one-line log explaining what happened; subsequent calls are silent.

For cases where you want to be explicit, use `get_local()` (same path, extra options for `cache_dir` / `format` / `freshness`), or pass `mode="live"` to hit the live Iceberg endpoint directly (useful for freshest data, OECD-restricted sources, or sliced queries with `limit=`/`start=`/`end=`):

```python
# Explicit cache+sync path with extra control
gdf = client.get_local("nz_parcels")
gdf = client.get_local("nz_parcels", cache_dir="/data/eolas", freshness="monthly")

# Force live scan — note: server returns 413 if the dataset is large/geo
# and no limit=/start=/end= filter is set; apply a filter or use mode="cached"
gdf = client.get("nz_parcels", mode="live")
```

See [Bulk downloads](../bulk-downloads.md) for the full routing rules and tier comparison.

Each returns a `Dataset` tagged with the source label.

## Discovery

```python
client.list()                    # all datasets — DataFrame
client.list("Stats NZ")          # filter by source
client.list_wellington()         # Wellington Region Councils only

client.search("HLFS")            # labour-force datasets (alias expansion)
client.search("OCR", source="RBNZ")
client.search("kapiti")          # → kcdc_* council layers
client.search("cpi")             # ranks rbnz_m1_prices before nz_cpi; prints CPI guidance
```

`nz_cpi` is OECD year-on-year % change, not a CPI index level — use `rbnz_m1_prices` for quarterly index levels.

## Dataset

All data-fetching methods return a `Dataset` — a pandas DataFrame subclass with extra metadata:

```python
df = client.statsnz("nz_cpi", start="2020-01-01")

print(df)
# Dataset: nz_cpi [Stats NZ]
# 20 rows
#          date  period   value
# 0  2020-01-01  2020Q1  1010.0
# ...

df.eolas_name    # "nz_cpi"
df.eolas_source  # "Stats NZ"
```

### Plotting

`Dataset` is a pandas `DataFrame` subclass, so any matplotlib, seaborn, or plotly workflow works directly. For a quick line chart:

```python
ax = df.plot(x="date", y="value")
ax.set_ylabel("Index (base 1000)")
```

Requires `matplotlib`: `pip install matplotlib`.

## Cache

Pass `cache=True` to avoid re-fetching the same series in a notebook session:

```python
client = Client("your_eolas_key", cache=True)

df1 = client.statsnz("nz_cpi")   # hits the API
df2 = client.statsnz("nz_cpi")   # returned from cache
```

## Working with large geo datasets

The 5.4M-row `linz.nz_parcels` table allocates ~10 GB when materialised as a GeoDataFrame. Pass `as_arrow=True` to skip all shapely allocation and get a zero-copy `pyarrow.Table` instead — geometry stays as Arrow buffers until you need it:

```python
# Zero-copy Arrow table — no shapely allocation
tbl = client.linz("nz_parcels", as_arrow=True)

# Filter before materialising — dramatically cheaper than loading the full GeoDataFrame
import duckdb
result = duckdb.sql("""
    SELECT parcel_id, geometry_wkt
    FROM tbl
    WHERE ST_Within(ST_GeomFromText(geometry_wkt),
                    ST_GeomFromText('POLYGON((174.7 -41.3, 174.8 -41.3, 174.8 -41.4, 174.7 -41.4, 174.7 -41.3))'))
""").df()
```

`as_arrow=True` works on all datasets (geo or non-geo), all routing modes (live, cached, auto), and all source helpers. It cannot be combined with `as_geo=True`.

## Polars output

```python
df = client.get("nz_cpi", engine="polars")
# returns a polars DataFrame
```

Requires `polars`: `pip install polars`.

## Exceptions

```python
from eolas_data.exceptions import RateLimitError, AuthenticationError, NotFoundError

try:
    df = client.statsnz("nz_cpi")
except RateLimitError:
    print("Upgrade to Pro for unlimited requests")
except AuthenticationError:
    print("Check your API key")
except NotFoundError:
    print("Series does not exist")
```

| Exception | HTTP status | When raised |
|---|---|---|
| `AuthenticationError` | 401, 403 | Invalid or inactive key |
| `RateLimitError` | 429 | Daily limit reached |
| `NotFoundError` | 404 | Series identifier not found |
| `APIError` | other | Unexpected API error |

## Attribution and provenance

Every `/data` response carries `X-Eolas-Attribution`, `X-Eolas-Licence`, and related
headers. The client merges them into `df.attrs["eolas_meta"]` automatically (v1.3.3+).

```python
df = client.get("rbnz_b1_exchange_rates_monthly", limit=5)
df.attrs["eolas_meta"]["attribution_text"]
df.attrs["eolas_meta"]["licence"]
```

For provenance in the JSON body (agents, pipelines), pass `envelope=True` — same as
`?envelope=1` on the API:

```python
df = client.get("nz_cpi", limit=5, envelope=True)
df.attrs["eolas_meta"]["data_sources"]  # licence block alongside rows
```

See [Getting started §5](../quickstart.md#5-attribution-and-provenance) for the raw HTTP
shape and Snowflake `ATTRIBUTIONS` table.

## Source

[github.com/phildonovan/eolas-data-python](https://github.com/phildonovan/eolas-data-python) · [PyPI](https://pypi.org/project/eolas-data/)
