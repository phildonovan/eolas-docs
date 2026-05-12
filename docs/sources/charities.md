# Charities Services data via eolas

[Charities Services](https://www.charities.govt.nz) (Te Rātā Atawhai) is the Department of Internal Affairs body that registers and regulates New Zealand's charitable trusts. eolas serves **6 datasets** from Charities Services — the full registry + annual financial returns + reference taxonomies.

If you're doing nonprofit-sector research, due diligence on a charity, policy analysis on philanthropy, or evaluating grant-applicant credibility — this is the source.

---

## What's in the catalogue

### Core registry

| Dataset | Description |
|---|---|
| `charities_organisations` | Master register of all currently-registered (and historical) NZ charities — name, registration number, status, location, registration date. |
| `charities_officers` | Trustees, directors, and other officers associated with each registered charity. |
| `charities_annual_returns` | Yearly financial returns — income, expenses, employees, volunteers — for each charity that has filed (most have, some haven't). |

### Reference taxonomies

| Dataset | Description |
|---|---|
| `charities_sectors` | Standardised sector classifications used by Charities Services (e.g. "Health", "Education", "Religion", "Sport"). |
| `charities_activities` | Standardised activity codes — what the charity actually does. |
| `charities_beneficiaries` | Standardised beneficiary codes — who the charity serves. |

---

## Refresh schedule

Monthly. Charities Services updates the registry continuously (new registrations, deregistrations, status changes); annual returns flow in throughout the year as each charity's filing deadline lands. Our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("charities_organisations")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Charities Services data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Charities Services (Department of Internal Affairs), served via eolas (eolas.fyi). CC-BY 4.0."*

A privacy note: data is regulator-published — names of officers + registered addresses are in the public registry by statute. Bank account numbers + private contact details are not in the open dataset.

---

## Common patterns

### How many active charities are there?

=== "Python"

    ```python
    orgs = client.charities("charities_organisations")
    active = orgs[orgs["status"] == "Registered"]
    print(f"Active NZ charities: {len(active):,}")
    print(f"Historical (deregistered or merged): {len(orgs) - len(active):,}")
    ```

=== "R"

    ```r
    orgs <- eolas_get_charities("charities_organisations")
    cat("Active:", sum(orgs$status == "Registered"), "\n")
    ```

### Top charities by income

```python
returns = client.charities("charities_annual_returns")
# Latest filed year per charity
latest = returns.sort_values("filing_year").groupby("charity_no").tail(1)
top = latest.sort_values("total_income", ascending=False).head(20)
print(top[["charity_name", "filing_year", "total_income"]])
```

### Charity-officer overlap

For governance / risk analysis — who serves on multiple boards:

```python
officers = client.charities("charities_officers")
# Count board memberships per officer
overlap = officers.groupby("officer_name").size().sort_values(ascending=False)
print(overlap.head(20))  # Often professional directors with 10+ boards
```

### Sector breakdown

```python
orgs = client.charities("charities_organisations")
sectors = client.charities("charities_sectors")
# Join to get human-readable sector names
combined = orgs.merge(sectors, on="sector_code", how="left")
print(combined.groupby("sector_name").size().sort_values(ascending=False))
```

---

## Source-specific notes

- **Status field is important**: "Registered" = currently active; "Deregistered" = removed (most often by their own request or after failing to file returns); "Removed" = removed by Charities Services for cause. Filter to "Registered" for any "active charities" analysis.
- **Annual return filing rate**: not every charity files on time. Smaller charities sometimes lag. For an "all charities" income total, filter to a year where filing is mostly complete (typically 2+ years before current).
- **Financial year varies**: each charity sets its own balance date — typically 31 March or 30 June. The `filing_year` field aligns to that charity's financial year, not a calendar year.
- **Reference tables for joins**: `charities_sectors`, `charities_activities`, and `charities_beneficiaries` are stable taxonomies. Join into `charities_organisations` for analysis by category.
- **Religious charities**: ~30% of registered charities are religious (Iwi trusts, churches, parish trusts). They face the same reporting requirements; the registry treats them uniformly.
- **Iwi trusts**: many post-Treaty-settlement iwi trusts are registered charities. They tend to have high revenue and complex governance — useful for Māori-sector economic research.

---

## Where to find more

- **Charities datasets on eolas**: [eolas.fyi/datasets?source=Charities+Services](https://eolas.fyi/datasets?source=Charities%20Services)
- **Charities Services portal**: [www.charities.govt.nz](https://www.charities.govt.nz)
- **Public registry search**: [register.charities.govt.nz](https://register.charities.govt.nz)
- **Annual returns + filings**: [www.charities.govt.nz/reporting](https://www.charities.govt.nz/reporting)

## Related

- [Stats NZ source guide](statsnz.md) — for non-profit-sector aggregate statistics
- [Examples](../examples/index.md) — worked code recipes
