# Python API reference

## `Client`

```python
class Client(api_key=None, base_url="https://api.virtus-solutions.io")
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str \| None` | `None` | Your `vs_...` key. Falls back to `VS_API_KEY` env var. |
| `base_url` | `str` | `"https://api.virtus-solutions.io"` | Override for testing. |

---

### `client.list()`

Return metadata for all available series.

```python
series = client.list()
# [{"name": "nz_cpi", "title": "NZ Consumer Price Index", "source": "OECD", ...}, ...]
```

**Returns:** `list[dict]`

---

### `client.info(name)`

Return metadata for a single series.

```python
meta = client.info("nz_cpi")
# {"name": "nz_cpi", "title": "NZ Consumer Price Index", "source": "OECD", ...}
```

**Parameters**

| Name | Type | Description |
|---|---|---|
| `name` | `str` | Series identifier, e.g. `"nz_cpi"` |

**Returns:** `dict`

**Raises:** `NotFoundError` if the series does not exist.

---

### `client.get(name, start=None, end=None, format="json")`

Fetch time-series data as a pandas DataFrame.

```python
df = client.get("nz_cpi", start="2020-01-01", end="2024-12-31")
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | — | Series identifier |
| `start` | `str \| None` | `None` | ISO date lower bound, e.g. `"2020-01-01"` |
| `end` | `str \| None` | `None` | ISO date upper bound |
| `format` | `str` | `"json"` | `"json"` or `"csv"` |

**Returns:** `pandas.DataFrame` with columns:

| Column | Type | Description |
|---|---|---|
| `date` | `datetime64` | Observation date |
| `period` | `str` | Period label, e.g. `"2023Q1"` |
| `value` | `float` | Observed value |
| `dimensions` | `str` | Extra breakdown dimensions (empty string if none) |

**Raises:** `NotFoundError`, `AuthenticationError`, `RateLimitError`

---

## Exceptions

All exceptions inherit from `vswarehouse.exceptions.VSWarehouseError`.

```python
from vswarehouse.exceptions import (
    VSWarehouseError,      # base
    AuthenticationError,   # 401 / 403
    RateLimitError,        # 429
    NotFoundError,         # 404
    APIError,              # other HTTP errors — has .status_code attribute
)
```
