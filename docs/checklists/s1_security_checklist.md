# SECURITY_CHECKLIST.md

## ✅ Application (Django)
- [ ] `DEBUG = False` in production  
- [ ] `SECRET_KEY` loaded from environment variables (never in Git)  
- [ ] `ALLOWED_HOSTS` restricted to domain(s)  
- [ ] `CSRF_COOKIE_SECURE = True`  
- [ ] `SESSION_COOKIE_SECURE = True`  
- [ ] `SECURE_HSTS_SECONDS > 0` (e.g. 31536000 for 1 year)  
- [ ] `SECURE_CONTENT_TYPE_NOSNIFF = True`  
- [ ] `SECURE_BROWSER_XSS_FILTER = True`  
- [ ] Database credentials stored in environment variables  

---

## ✅ Server (Linux + Gunicorn/Uvicorn + Nginx)
- [ ] Non-root deployment user created  
- [ ] Firewall (UFW/iptables) allows only SSH (22), HTTP (80), HTTPS (443)  
- [ ] Gunicorn/Uvicorn running as systemd service  
- [ ] Log rotation configured (`journalctl` or logrotate)  
- [ ] SSH key authentication enabled, password login disabled  

---

## ✅ TLS / HTTPS
- [ ] Nginx reverse proxy configured with HTTPS  
- [ ] Let’s Encrypt certificate installed via Certbot  
- [ ] Automatic certificate renewal enabled (`certbot renew`)  
- [ ] Redirect HTTP → HTTPS enforced  

---

## ✅ Payment (Stripe)
- [ ] API keys stored in environment variables  
- [ ] Webhook endpoint secured with Stripe signature verification  
- [ ] Test mode enabled (no real charges in Sprint 1)  

---

## ✅ Email (Postmark / SES)
- [ ] SMTP credentials stored in environment variables  
- [ ] TLS enabled for all email connections  
- [ ] Sandbox mode enabled (no live customer emails in Sprint 1)  

---

## ✅ DNS / CDN (Cloudflare)
- [ ] Domain DNS configured to point to VPS  
- [ ] Cloudflare proxy enabled (orange cloud)  
- [ ] SSL/TLS mode set to “Full (Strict)”  
- [ ] Web Application Firewall (WAF) enabled  
- [ ] DDoS protection enabled (default with Cloudflare)  

---

## ✅ Monitoring & Logging
- [ ] `/health` endpoint accessible and tested in production  
- [ ] Basic uptime monitoring configured (e.g. UptimeRobot, Healthchecks.io)  
- [ ] Error logs accessible via systemd and Django logs  

---

## ✅ Git Versioning
- [ ] All changes committed with descriptive messages  
- [ ] Security checklist fully reviewed before tagging  
- [ ] Tag created: `git tag v0.0.1 -m "Sprint 1 secure walking skeleton"`  
- [ ] Tag pushed to remote: `git push origin v0.0.1`

