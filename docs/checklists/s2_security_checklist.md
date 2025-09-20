# SECURITY_CHECKLIST_SPRINT_2.md

> Scope: harden the MVP e‑commerce slice introduced in Sprint 2 (auth, real payments, downloads, email). This complements the Sprint 1 checklist and **does not replace it**.

---

## ✅ Application (Django)
- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` set to exact domains
- [ ] `SECRET_KEY` and all credentials loaded **only** from environment/secret store
- [ ] `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS ≥ 31536000`, include subdomains if applicable
- [ ] `SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"`
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [ ] `X_FRAME_OPTIONS = "DENY"`
- [ ] Default `CSP` defined (see section below)
- [ ] Admin URL randomized (not `/admin/`) and restricted (IP allowlist or 2FA)

---

## ✅ Authentication & Accounts
- [ ] Passwords hashed with **Argon2** (preferred) or PBKDF2 w/ strong iterations
- [ ] Login rate limiting (per IP & per account) via middleware/WAF
- [ ] Session timeout & re-auth on sensitive actions (checkout, email change)
- [ ] Email verification required before granting download access
- [ ] Optional: SSO (“Login with…”) only if securely configured
- [ ] Account deletion/export endpoints planned (GDPR basics)

---

## ✅ Payments (Stripe – live mode readiness)
- [ ] Distinct keys for **test** and **live**, never mixed
- [ ] Webhook signature **verified** with `STRIPE_WEBHOOK_SECRET`
- [ ] Webhook endpoint reachable only via HTTPS; idempotency handled
- [ ] Prices and product IDs pulled from Stripe **or** validated against DB
- [ ] Order state machine defined (created → paid → fulfilled)
- [ ] Refund/chargeback flow considered (mark order & revoke downloads)
- [ ] PII/PCI: no card data ever stored on our side

---

## ✅ Storage & Downloads (Backblaze B2)
- [ ] Buckets **private** only; no public ACLs
- [ ] Presigned URLs short‑lived (≤ 10 min) and single‑use if possible
- [ ] Download authorization bound to **paid** orders & user/session
- [ ] Optional: IP pinning and bandwidth throttling
- [ ] File paths/IDs not guessable; no user‑controlled path joins
- [ ] Virus/malware scanning for uploaded assets (if any user uploads in future)

---

## ✅ Email (Postmark / SES)
- [ ] SPF/DKIM/DMARC all **valid** on the sender domain
- [ ] Transactional templates stored server‑side; inputs sanitized/escaped
- [ ] No secrets in email content or URLs
- [ ] Unsubscribe footer not required for pure transactional, but add contact info

---

## ✅ TLS / HTTPS (Nginx + Let’s Encrypt)
- [ ] Redirect HTTP → HTTPS enforced
- [ ] TLS config with modern ciphers; TLS1.2+ only
- [ ] OCSP stapling enabled (if available)
- [ ] Auto‑renew for certificates verified

---

## ✅ Cloudflare / WAF / Rate Limiting
- [ ] Proxy (orange cloud) enabled; SSL mode **Full (Strict)**
- [ ] WAF Core Rules on; bot fight mode considered
- [ ] Rate limits on login, webhook, download routes (burst + sustained caps)
- [ ] Country/ASN blocks if relevant (optional)

---

## ✅ Secrets & Configuration
- [ ] `.env` not in Git; production secrets via environment or secret manager
- [ ] Separate **test** vs **live** configs for Stripe, email, B2
- [ ] Rotate keys on compromise or role change; document rotation playbook

---

## ✅ Monitoring, Logging & Auditing
- [ ] Uptime probe on `/health` (public) and internal app checks
- [ ] Application logs (info, warning, error) with request IDs & user IDs (if logged in)
- [ ] Access logs for downloads (who/when/what)
- [ ] Alerting on webhook failures, payment errors, 5xx spikes
- [ ] Log retention policy defined; no sensitive data in logs

---

## ✅ Data Protection (GDPR‑lite)
- [ ] Privacy Policy and Terms linked in footer
- [ ] Data minimization: collect only necessary fields
- [ ] User can request data export/delete (manual process acceptable at MVP)
- [ ] Backups encrypted at rest; restore tested (see below)

---

## ✅ Backups & Recovery
- [ ] PostgreSQL automated backups (daily) + point‑in‑time if possible
- [ ] Off‑site backup for critical assets (B2 or object storage)
- [ ] Periodic **restore test** documented

---

## ✅ Content Security Policy (CSP) – baseline
- [ ] Example strict CSP (adapt domains to project):
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://js.stripe.com;
  frame-src https://js.stripe.com https://hooks.stripe.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.stripe.com;
  base-uri 'self';
  frame-ancestors 'none';
  form-action 'self' https://checkout.stripe.com;
```
- [ ] Report‑Only mode first; tighten iteratively

---

## ✅ Go‑Live Gates (Sprint 2)
- [ ] Test payments (test mode) → switch to live → test live micro‑transaction
- [ ] End‑to‑end flow: anon user → create account → buy → receive email → download
- [ ] Security smoke tests: login throttling, webhook tamper, expired URL download
- [ ] Sign‑off recorded; tag release **v2.0.0** (see VERSIONS_SPRINT_2.md)

