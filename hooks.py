"""MkDocs event hooks (separate from mkdocs-macros)."""

import os


def _env_flag(name: str, *, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() not in (
        "",
        "0",
        "false",
        "no",
        "off",
    )


_DEFAULT_BETA_BANNER_MESSAGE = (
    "Full launch coming soon — explore the data and sign up for early access."
)


def on_config(config):
    config.extra["beta_banner"] = _env_flag("EOLAS_BETA_BANNER")
    custom = os.environ.get("EOLAS_BETA_BANNER_MESSAGE", "").strip()
    config.extra["beta_banner_message"] = custom or _DEFAULT_BETA_BANNER_MESSAGE