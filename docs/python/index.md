# Python client

The `vswarehouse` Python package provides a `Client` class that wraps the vs-warehouse REST API and returns **pandas DataFrames**.

## Installation

```bash
pip install vswarehouse
```

Requires Python 3.10+ and pandas 1.5+.

## Initialisation

```python
from vswarehouse import Client

# Pass key directly
client = Client("vs_your_key")

# Or read from VS_API_KEY environment variable
client = Client()
```

## Methods at a glance

| Method | Returns | Description |
|---|---|---|
| `client.list()` | `list[dict]` | All available series with metadata |
| `client.info(name)` | `dict` | Metadata for one series |
| `client.get(name, ...)` | `DataFrame` | Time-series data |

## Exceptions

Import from `vswarehouse.exceptions` or catch at the base class:

```python
from vswarehouse import Client
from vswarehouse.exceptions import RateLimitError, AuthenticationError, NotFoundError

try:
    df = client.get("nz_cpi")
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
| `RateLimitError` | 429 | Free-tier daily limit reached |
| `NotFoundError` | 404 | Series identifier not found |
| `APIError` | other | Unexpected API error |

## Source

[github.com/phildonovan/vswarehouse-python](https://github.com/phildonovan/vswarehouse-python) · [PyPI](https://pypi.org/project/vswarehouse/)
