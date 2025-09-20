## Sprint 3 — Open Roadmap (Portfolio‑oriented)
> Intent: move from MVP to a polished, portfolio‑grade product, balancing scope with professional standards. Timeboxes are indicative; refine per capacity.

### Themes (not exhaustive)
- **Customer Experience**: search, filters, tags, collections, better checkout flow
- **Account Area**: order history, re‑download purchases, profile, invoices (PDF)
- **Catalog Ops**: batch upload products, images, pricing rules (promo codes)
- **Quality & Observability**: structured logging, metrics, error tracking (Sentry), CI
- **Hardening**: backups automation, restore drills, CSP strict mode, 2FA admin
- **Performance**: caching headers, CDN tuning, image optimization

### Possible Version Stream (coarse‑grained)
- **v2.1.0**: Customer accounts area (orders list, re‑download) — 10–20 h
- **v2.2.0**: Catalog filters & search — 10–16 h
- **v2.3.0**: Promo codes / coupons (Stripe) — 8–12 h
- **v2.4.0**: Invoices PDF + email attachment — 8–12 h
- **v2.5.0**: Admin batch upload & media management — 10–20 h
- **v2.6.0**: Observability (Sentry, metrics, dashboards) — 6–10 h
- **v2.7.0**: Security hardening (2FA admin, CSP strict, backups) — 8–16 h
- **v2.8.0**: Polished UI theme & marketing pages — 12–24 h
- **v3.0.0**: Portfolio Release — public demo + case study page

### Portfolio Deliverables
- Public demo URL with seeded data
- **Case Study** page: problem → approach (AI‑assisted) → architecture → features → security → results
- Screenshots/recordings of key flows (catalog, checkout, download)
- Technical write‑up: Walking Skeleton → Tracer Bullet → MVP → polish

### Guardrails (to avoid underestimation)
- Keep vertical slices end‑to‑end (usable at each tag)
- Maintain security gates per release (reuse Sprint 1/2 checklists)
- Resist scope creep: defer “nice‑to‑have” to later tags

---

## 6) Final Notes
- This document **locks** the dev environment setup and its evolution per version.
- Sprint 3 is intentionally open to let us steer toward a portfolio‑ready product without over‑specifying.
- For any change, bump a minor version of this doc (e.g., `v1.1`), record deltas.

