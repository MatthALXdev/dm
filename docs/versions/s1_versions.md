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

### v0.2.0 - UI Moderne + Infrastructure nginx-static
- **Feature** : Template `base.html` avec Tailwind CSS via CDN
- **Feature** : Refonte complète catalog, product, thanks pages
- **Feature** : Design responsive (mobile/tablet/desktop)
- **Feature** : Branding "Pyxalix" (couleurs indigo, header/footer)
- **Feature** : Parcours utilisateur complet avec mock payment
- **Feature** : Vues `purchase()` et `thanks()` ajoutées
- **Infra** : Architecture 3 docker-compose (dev/nexus/vps)
- **Infra** : Service nginx-static mutualisé pour media files (100x plus rapide)
- **Infra** : Traefik routing avec priorités (nginx priority 100, Django priority 1)
- **Infra** : Migration 0003 pour chargement initial des produits (remplace seed.py)
- **Infra** : Images produits avec noms fixes (pas de hash Django)
- **Infra** : CSRF_TRUSTED_ORIGINS configuré pour HTTPS production
- **Infra** : Tests validés sur Nexus avec Traefik HTTP
- **Infra** : Containers : `pyx_web`, `pyx_postgres`, `nexus_nginx_static`
- **Docs** : DOCKER-COMPOSE-CONFIGS.md (guide complet)
- **Docs** : INFRASTRUCTURE.md (architecture nginx-static)
- **Docs** : /nexus/shared/README.md (services mutualisés)
- **Docs** : Workflow Git branches (develop-extern/develop-home/main)
- **UX** : Hover effects, transitions, gradient placeholders
- **Fix** : Media files 404 en production (nginx sert les fichiers au lieu de Django)
- **Fix** : CSRF 403 en HTTPS sur VPS (trusted origins)
- **Refactor** : Suppression de seed.py (remplacé par migration)
- **Refactor** : Nettoyage volumes Docker (media_data retiré)
- **Refactor** : Suppression scripts obsolètes (7 fichiers bootstrap/audit Windows PS1)
- ⏱️ Temps réel : **9 h** (UI 4h + Infra 5h)

### v0.2.1 - Rebrand Pyxalix → Pyx
- **Refactor** : Rebrand complet Pyxalix → Pyx (nom commercial)
- **Config** : docker-compose.yml - domaine `pyx.devamalix.fr`, containers `pyx_web/pyx_postgres`, network `pyx-network`
- **Config** : docker-compose.nexus.yml - domaine `pyx.nexus.local`, router `pyx-web-nexus`
- **Config** : docker-compose.dev.yml - commentaires mis à jour
- **Docs** : README.md - nomenclature explicite (commercial "Pyx" vs technique "DM")
- **Docs** : 17 fichiers documentation - remplacements globaux (domaines, containers, networks)
- **UI** : 5 templates HTML - "Pyxalix" → "Pyx" (tous affichages utilisateur)
- **Docs** : s1_e5.md - documentation sprint rebrand
- **Breaking** : Déploiement VPS nécessite DNS OVH (`pyx.devamalix.fr`), modification `.env` manuelle, redémarrage containers
- **Note** : Repository GitHub reste `dm` (nom technique inchangé)
- ⏱️ Temps réel : **1 h 30** (modifications + doc sprint)

### v0.3.0 (prévu)
- Intégration Stripe Checkout (session test)
- Modèle `Order` minimal
- Bouton paiement fonctionnel
- ⏱️ Estimation : **4–6 h**

### v0.4.0 (prévu)
- Webhook Stripe implémenté
- Création d'un `Order` en DB après paiement
- Page `/thanks` avec retour utilisateur
- ⏱️ Estimation : **4–8 h**

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
- Déploiement sur VPS OVH (37.59.115.242)
- Traefik + HTTPS Let's Encrypt
- Domain : `pyx.devamalix.fr`
- ⏱️ Estimation : **2–4 h** (infra déjà prête)

### v1.0.0
- Tests unitaires + E2E (end-to-end)
- Monitoring `/health` activé
- Walking Skeleton complet livré
- ⏱️ Estimation : **8–16 h**