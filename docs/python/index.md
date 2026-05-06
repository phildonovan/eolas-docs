# Python client

The `vswarehouse` Python package provides a `Client` class that wraps the vs-warehouse REST API and returns **`VSeries` objects** — pandas DataFrames with source metadata and a built-in plot method.

## Installation

```bash
pip install vswarehouse
```

Optional extras:

```bash
pip install vswarehouse[polars]      # polars output support
pip install vswarehouse[plot]        # matplotlib for plot_series()
```

Requires Python 3.10+ and pandas 1.5+.

## Initialisation

```python
from vswarehouse import Client

# Pass key directly
client = Client("vs_your_key")

# Read from VS_API_KEY environment variable
client = Client()

# With in-memory cache (great for notebooks)
client = Client("vs_your_key", cache=True)
```

## Source-specific helpers

The recommended way to fetch data — the source is encoded in the method name, making code self-documenting and autocomplete-friendly:

```python
df = client.statsnz("nz_cpi", start="2020-01-01")   # Stats NZ
df = client.oecd("nz_gdp")                           # OECD
df = client.rbnz("ocr")                              # RBNZ
df = client.treasury("treasury_fiscal_spending")      # NZ Treasury
df = client.linz("nz_parcels")                       # LINZ
```

Each returns a `VSeries` tagged with the source label.

## Discovery

```python
client.list()              # all series — list of dicts
client.list("Stats NZ")   # filter by source
```

## VSeries

All data-fetching methods return a `VSeries` — a pandas DataFrame subclass with extra metadata:

```python
df = client.statsnz("nz_cpi", start="2020-01-01")

print(df)
# VSeries: nz_cpi [Stats NZ]
# 20 rows
#          date  period   value
# 0  2020-01-01  2020Q1  1010.0
# ...

df.vs_name    # "nz_cpi"
df.vs_source  # "Stats NZ"
```

### `.plot_series()`

Quick matplotlib line chart — returns the `Axes` object for further customisation:

```python
ax = df.plot_series()
ax.set_ylabel("Index (base 1000)")   # add to the returned axes
```

Requires `matplotlib`: `pip install matplotlib`.

## Cache

Pass `cache=True` to avoid re-fetching the same series in a notebook session:

```python
client = Client("vs_your_key", cache=True)

df1 = client.statsnz("nz_cpi")   # hits the API
df2 = client.statsnz("nz_cpi")   # returned from cache
```

## Polars output

```python
df = client.get("nz_cpi", engine="polars")
# returns a polars DataFrame
```

Requires `polars`: `pip install polars`.

## Exceptions

```python
from vswarehouse.exceptions import RateLimitError, AuthenticationError, NotFoundError

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

## Source

[github.com/phildonovan/vswarehouse-python](https://github.com/phildonovan/vswarehouse-python) · [PyPI](https://pypi.org/project/vswarehouse/)
