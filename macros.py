"""mkdocs-macros hook: fetch live counts from the eolas.fyi API at build time.

Variables exposed to markdown templates:
    {{ dataset_count }}  rounded-down dataset count, e.g. "710" when live is 717
    {{ sources }}        human-readable source list, e.g. "Stats NZ, OECD, RBNZ, ..."
    {{ source_count }}   number of distinct sources
    {{ series_count }}   alias for dataset_count, kept for back-compat with old docs

Falls back to safe defaults if the API is unreachable so docs builds never break.
"""
import requests

API = "https://api.eolas.fyi/v1/datasets"
FALLBACK = {"dataset_count": 700, "sources": "Stats NZ, OECD, RBNZ, NZ Treasury, LINZ, Stats NZ Geospatial, MBIE, Waka Kotahi, MSD, NZ Police / MoJ, ACC, Education Counts, WorkSafe NZ", "source_count": 13}


def _fetch():
    r = requests.get(API, timeout=10)
    r.raise_for_status()
    data = r.json()
    sources = sorted({s["source"] for s in data})
    return {
        "dataset_count": (len(data) // 10) * 10,
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
