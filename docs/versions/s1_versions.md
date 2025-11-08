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

## 🎯 Versions restantes Sprint 1 (révisées)


### v0.3.0 ⏳ EN ATTENTE - Intégration Stripe Checkout
**Objectif** : Remplacer mock payment par paiement Stripe test mode

**Features :**
- Installation SDK Stripe Python
- Configuration clés API Stripe (test mode)
- Modèle `Order` basique (product, stripe_session_id, amount, status, timestamps)
- Vue création Stripe Checkout Session
- Redirection vers Stripe hosted page
- Gestion URLs success/cancel
- Bouton "Acheter maintenant" appelle endpoint checkout
- Page `/thanks` affiche confirmation avec session_id

**Config :**
- Variables environnement Stripe (public/secret/webhook keys)

**Docs :**
- Guide configuration Stripe
- README section "Paiement" mise à jour

⏱️ **Estimation : 4–6 h**

---

### v0.4.0 ⏳ PLANIFIÉ - Webhook Stripe + Création Order
**Objectif** : Automatiser création Order après paiement validé

**Features :**
- Endpoint webhook Stripe (POST)
- Vérification signature Stripe
- Gestion event `checkout.session.completed`
- Création Order en DB avec status='paid'
- Logging succès/échec
- Sécurisation endpoint (CSRF exempt, validation signature, rate limiting)
- Configuration webhook Stripe Dashboard
- Amélioration page `/thanks` avec détails Order
- Gestion cas session invalide

**Docs :**
- Guide webhook Stripe
- Section troubleshooting Stripe

⏱️ **Estimation : 4–8 h**

---

### v0.5.0 ⏳ PLANIFIÉ - Tests Unitaires
**Objectif** : Couvrir models, views et intégration Stripe

**Tests à créer :**
- Tests Models (Product creation, str, slug unique, Order creation, status default)
- Tests Views (catalog 200, display products, product detail valid/invalid slug, purchase redirect)
- Tests Stripe (checkout session creation, webhook signature valid/invalid, order creation après event)
- Tests Migrations (vérification chargement 3 produits initiaux)

**Configuration :**
- pytest.ini et conftest.py
- Coverage minimum : 70%
- Commande pytest avec coverage HTML

**Docs :**
- Guide tests complet
- README section "Tests" avec badge coverage

⏱️ **Estimation : 6–8 h**

---

### v0.6.0 ⏳ PLANIFIÉ - CI/CD GitHub Actions
**Objectif** : Automatiser tests sur chaque push

**Workflow :**
- Trigger sur push (main, develop branches) et pull requests
- Service PostgreSQL pour tests
- Setup Python 3.11 avec cache pip
- Installation dépendances
- Migrations de test
- Exécution tests avec coverage
- Upload coverage vers Codecov

**GitHub Secrets :**
- Clés Stripe test mode

**Badges README :**
- Badge CI Tests
- Badge Coverage

**Docs :**
- Guide CI/CD
- README section "CI/CD"

⏱️ **Estimation : 2–3 h**

---

### v1.0.0 🎯 OBJECTIF SPRINT 1 - Walking Skeleton Complet
**Objectif** : Projet e-commerce CORE fonctionnel avec paiement + tests + CI/CD

**Récapitulatif features :**
- Catalog + Product pages responsive
- Infrastructure Docker + nginx-static + Traefik
- Déploiement VPS HTTPS
- Paiement Stripe Checkout fonctionnel
- Webhook Stripe + création Order automatique
- Tests unitaires (coverage > 70%)
- CI/CD GitHub Actions
- Documentation complète

**Tests finaux production :**
- Achat produit sur pyx.devamalix.fr
- Vérification Order en DB
- Vérification webhook logs
- Badge CI vert sur GitHub
- Coverage report accessible

**Livrables finaux :**
- README avec badges (CI + Coverage)
- Screenshot parcours utilisateur
- Documentation technique complète
- Repo prêt pour démonstration alternance

**Démo entretien :**
> "E-commerce avec paiement Stripe intégré, déployé en production VPS HTTPS, tests automatisés (coverage 70%+) et CI/CD GitHub Actions."

⏱️ **Estimation finale : 2–4 h** (validation + docs finales)

---

## 📊 Récapitulatif Sprint 1

### Temps total Sprint 1

| Phase | Versions | Temps réel | Status |
|-------|----------|------------|--------|
| **Foundation** | v0.0.1 → v0.1.2 | 10h | ✅ Accompli |
| **UI + Infra** | v0.2.0 → v0.2.2 | 12.5h | ✅ Accompli |
| **Stripe** | v0.3.0 → v0.4.0 | 8-14h | ⏳ Reste à faire |
| **Tests + CI/CD** | v0.5.0 → v0.6.0 | 8-11h | ⏳ Reste à faire |
| **Finalisation** | v1.0.0 | 2-4h | ⏳ Reste à faire |

**Total Sprint 1 :** 40.5-51.5h (22.5h fait + 18-29h reste)

**Temps restant estimé :** 18-29h (2.5-4 jours de travail)

---

## 🎯 Prochaines étapes immédiates

1. **v0.3.0** - Intégration Stripe Checkout (4-6h)
2. **v0.4.0** - Webhook + Order (4-8h)
3. **v0.5.0** - Tests unitaires (6-8h)
4. **v0.6.0** - CI/CD (2-3h)
5. **v1.0.0** - Validation finale (2-4h)

**Deadline recommandée Sprint 1 :** Dans 3-4 jours

---

## 📝 Notes importantes

### Changements vs version originale
- ✅ v0.7.0 (UI responsive) : **Fusionnée dans v0.2.0** (déjà fait)
- ✅ v0.9.0 (Déploiement VPS) : **Renommée v0.2.2** (déjà fait)
- ❌ v0.8.0 (Sécurité prod) : **Reportée Sprint 2** (HSTS, CSP pas critiques pour alternance)
- ❌ Backblaze B2 : **Reporté Sprint 2** (pas critique pour démo)
- ❌ Email transactionnel : **Reporté Sprint 2** (pas critique pour démo)

### Justification
Focus sur **paiement réel + tests + CI/CD**.
Téléchargement et email peuvent être ajoutés après (Sprint 2).
---

**Dernière mise à jour :** 08 novembre 2025  
**Status :** Sprint 1 à 40% (v0.0.1 → v0.2.2 accompli)  
**Prochaine version :** v0.3.0 - Stripe Checkout
