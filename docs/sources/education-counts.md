# Education Counts data via eolas

[Education Counts](https://www.educationcounts.govt.nz) is the Ministry of Education's official statistics portal — covering schools, early childhood education (ECE), tertiary institutions, attendance, attainment, funding, and outcomes. eolas serves **38 datasets** from Education Counts.

If you're doing education-policy research, school-performance analysis, demographic + enrolment forecasting, or labour-market follow-on analysis (qualification → wages) — this is the source.

---

## What's in the catalogue

### Schools — counts + characteristics

| Dataset | Description |
|---|---|
| `edcounts_number_of_schools` | Annual count of NZ schools at 1 July, by sector (primary / composite / secondary / special), authority (state / state-integrated / private), and region. |
| `edcounts_attendance` | Regular + provisional attendance rates by term, year, region, decile, year level. |
| `edcounts_homeschooling` | Annual homeschooled student counts by region + year level. |
| `edcounts_ors` | Annual count of ORS (Ongoing Resourcing Scheme) students — special education funding for high-needs children. |

### Funding

| Dataset | Description |
|---|---|
| `edcounts_funding_to_schools` | Annual operational + resourcing funding to NZ schools, by funding type, school sector, and region. |
| `edcounts_finances` | Broader education-system finances. |
| `edcounts_apprenticeship_boost` | Apprenticeship Boost scheme payments + recipient counts. |

### Student support

| Dataset | Description |
|---|---|
| `edcounts_financial_support_for_students` | Student support payments + recipient counts. |
| `edcounts_fees_free` | Fees-Free tertiary policy uptake + funding (2018+). |

### Achievement + outcomes

| Dataset | Description |
|---|---|
| `edcounts_achievement_and_attainment` | NCEA + UE achievement statistics. |
| `edcounts_beyond_study` | Post-study outcomes (employment, earnings, further study). |
| `edcounts_early_leaving_exemptions` | Early-leaving exemptions granted. |
| `edcounts_reading_recovery` | Reading Recovery programme participation + outcomes. |

### Tertiary + international

| Dataset | Description |
|---|---|
| `edcounts_international_students` | Annual international student enrolments by country of origin, education sector, region. |
| `edcounts_initial_teacher_education` | Teacher-training programme enrolments + completions. |
| `edcounts_micro_credentials` | Micro-credential enrolments (NZQA-approved short courses). |

### Language + cultural

| Dataset | Description |
|---|---|
| `edcounts_maori_language_in_schooling` | Te reo Māori-medium + immersion school participation. |
| `edcounts_pacific_language_in_schooling` | Pacific language education participation. |
| `edcounts_language_use_in_ece` | Language of instruction in ECE settings. |

Plus 18+ other datasets covering specific programmes + cohorts. Browse: [eolas.fyi/datasets?source=Education+Counts](https://eolas.fyi/datasets?source=Education%20Counts).

---

## Refresh schedule

Quarterly. Education Counts publishes most series annually (after each academic year closes), with quarterly updates to attendance + enrolment series. Our refresh runs weekly to catch new releases promptly.

```python
meta = client.info("edcounts_number_of_schools")
meta["last_refreshed_at"]
meta["source_last_modified_at"]
```

---

## License

All Education Counts data is published under **[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Commercial use is fine; attribution required.

Recommended attribution: *"Source: Education Counts (Ministry of Education), served via eolas (eolas.fyi). CC-BY 4.0."*

---

## Common patterns

### School-attendance trend

=== "Python"

    ```python
    att = client.education_counts("edcounts_attendance", start="2018-01-01")
    by_term = att.groupby(["year", "term"])["regular_attendance_rate"].mean().reset_index()
    by_term.plot(x="term", y="regular_attendance_rate", title="NZ school regular attendance rate")
    ```

=== "R"

    ```r
    library(ggplot2)
    att <- eolas_get_education_counts("edcounts_attendance", start = "2018-01-01")
    ggplot(att, aes(date, regular_attendance_rate)) + geom_line() +
      labs(title = "NZ school regular attendance rate")
    ```

### Schools count + composition

```python
schools = client.education_counts("edcounts_number_of_schools")
# Latest year, by sector
latest = schools[schools["year"] == schools["year"].max()]
print(latest.groupby("sector")["count"].sum().sort_values(ascending=False))
```

### International student source countries

```python
intl = client.education_counts("edcounts_international_students")
# Latest year, top countries
latest = intl[intl["year"] == intl["year"].max()]
top = latest.groupby("country")["enrolments"].sum().sort_values(ascending=False).head(15)
print(top)
```

---

## Source-specific notes

- **NZ school year = calendar year**: terms 1-4 run February-December. "2024" data means full 2024 academic year.
- **Decile system retired in 2023**: schools are now classified by Equity Index (EQI) — a continuous score. Older Education Counts datasets reference decile; newer use EQI. Some series carry both for continuity.
- **Attendance rates**: "regular" = present > 90% of half-days. "Provisional" = > 80%. Different rates aren't directly comparable across series — check the methodology in source metadata.
- **State-integrated vs state**: state schools are fully state-funded; state-integrated (often religious) have some private character but accept state funding. Count separately for compositional analysis.
- **ORS funding cohort is small but high-cost**: ~10,000 students receive ORS funding for high learning needs. Per-student cost much higher than mainstream.
- **Tertiary data lags**: most tertiary statistics are 12-18 months after the calendar year (allows for full enrolment + completion reconciliation). 2023 data was published mid-to-late 2024.

---

## Where to find more

- **Education Counts datasets on eolas**: [eolas.fyi/datasets?source=Education+Counts](https://eolas.fyi/datasets?source=Education%20Counts)
- **Education Counts portal**: [www.educationcounts.govt.nz](https://www.educationcounts.govt.nz)
- **Ministry of Education**: [www.education.govt.nz](https://www.education.govt.nz)

## Related

- [Stats NZ source guide](statsnz.md) — for school-age population denominators
- [MSD source guide](msd.md) — for Student Allowance + Student Loan data
- [Examples](../examples/index.md) — worked code recipes
