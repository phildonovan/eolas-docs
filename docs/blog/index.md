# Blog

Technical notes from building and maintaining eolas. Mostly investigations, fixes, and honest accounts of what took longer than it should have.

---

## 2026

- **[Reading our own GeoParquet was harder than it should have been](2026-05-27-geoparquet-rabbit-hole.md)** — 2026-05-27
  Why `eolas_get_linz("nz_parcels")` was printing confusing warnings and running 95 seconds, what the actual root cause was (NULL geometries in `sf::st_as_sfc.WKB`), the fix, and where Iceberg v3 fits in the long-term picture.
