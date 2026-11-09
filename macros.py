"""mkdocs-macros hook: fetch the live source list from the eolas.nz API at build time.

Variables exposed to markdown templates:
    {{ dataset_count }}  durable catalogue floor, always "1,500" (not the live total)
    {{ sources }}        human-readable source list, e.g. "Stats NZ, OECD, RBNZ, ..."
    {{ source_count }}   number of distinct sources
    {{ series_count }}   alias for dataset_count, kept for back-compat with old docs

The live catalogue size is not interpolated. Publishing it (or rounding it down
to the nearest 10) produced the stale "1530+" figure. Pages should say 1,500+.

Falls back to safe defaults if the API is unreachable so docs builds never break.
"""
import requests

API = "https://api.eolas.nz/v1/datasets"
# Durable floor. Do not publish len(datasets) or a nearest-10 rounding of it.
DATASET_COUNT = "1,500"
FALLBACK = {
    "dataset_count": DATASET_COUNT,
    "sources": (
        "Stats NZ, OECD, RBNZ, NZ Treasury, LINZ, Stats NZ Geospatial, MBIE, Waka Kotahi, "
        "MSD, NZ Police / MoJ, ACC, Education Counts, WorkSafe NZ, PHARMAC, EECA, DOC, "
        "and regional councils"
    ),
    "source_count": 34,
}


def _fetch():
    r = requests.get(API, timeout=10)
    r.raise_for_status()
    data = r.json()
    sources = sorted({s["source"] for s in data})
    return {
        "dataset_count": DATASET_COUNT,
        "sources": ", ".join(sources),
        "source_count": len(sources),
    }


def define_env(env):
    try:
        values = _fetch()
    except Exception as e:
        print(f"[macros] API fetch failed ({e}), using fallback")
        values = FALLBACK
    for k, v in values.items():
        env.variables[k] = v
    # Back-compat alias for any pages that still reference series_count
    env.variables["series_count"] = values["dataset_count"]
