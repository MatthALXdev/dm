# VERSIONS.md

## 🚀 Sprint 1 — Versions & Deliverables

### v0.0.1
- Repo initial créé
- Django project démarré (`hello world`)
- `python manage.py runserver` fonctionne
- ⏱️ Estimation : **0.5–1 h**

### v0.0.2
- Endpoint `/health`
- Page d’accueil `/home`
- ⏱️ Estimation : **1–2 h**

### v0.1.0
- Modèle `Product`
- Pages `catalog` et `product` (détail)
- ⏱️ Estimation : **4–8 h**

### v0.1.1
- Dockerisation complète (PostgreSQL 16 + Django 5.2.6)
- Docker Compose avec hot-reload et healthcheck
- Configuration `.env.docker.example`
- Script d'initialisation pour Linux/Nexus
- ⏱️ Temps réel : **2 h**

### v0.1.2 - Fixes & Configuration
- **Fix** : Chargement variables d'environnement (passage de `env_file` à interpolation `${VAR}`)
- **Fix** : Healthcheck PostgreSQL corrigé (`pg_isready -d dm_db`)
- **Feature** : Fixtures Django avec 3 produits de test (`core/fixtures/initial_data.json`)
- Migration de `.env.docker` vers `.env` (convention Docker Compose)
- README mis à jour avec documentation environnements local + Nexus
- ⏱️ Temps réel : **2 h 30**

### v0.2.0
- Intégration Stripe Checkout (session test)
- Bouton paiement fonctionnel
- ⏱️ Estimation : **3–6 h**

### v0.2.1
- Page `/thanks` (retour utilisateur après paiement)
- ⏱️ Estimation : **0.5–1 h**

### v0.3.0
- Webhook Stripe implémenté
- Création d’un `Order` minimal en DB
- ⏱️ Estimation : **4–8 h**

### v0.4.0
- Génération d’un token de téléchargement (mock)
- ⏱️ Estimation : **2–4 h**

### v0.5.0
- Intégration Backblaze B2
- Génération d’URL presignées réelles
- ⏱️ Estimation : **4–8 h**

### v0.6.0
- Email transactionnel envoyé (Postmark/SES sandbox)
- ⏱️ Estimation : **2–4 h**

### v0.7.0
- UI MVP responsive (mobile-friendly)
- ⏱️ Estimation : **8–16 h**

### v0.8.0
- Sécurité prod minimale activée (HSTS, CSP, headers sécurisés)
- ⏱️ Estimation : **3–6 h**

### v0.9.0
- Déploiement sur VPS Hetzner
- Nginx + systemd configurés
- HTTPS via Cloudflare (Full Strict)
- ⏱️ Estimation : **8–16 h**

### v1.0.0
- Tests unitaires + E2E (end-to-end)
- Monitoring `/health` activé
- Walking Skeleton complet livré
- ⏱️ Estimation : **8–16 h**