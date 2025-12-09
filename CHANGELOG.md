# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [Unreleased]

### À venir
- v0.5.0: Tests unitaires automatisés (pytest + coverage)
- v0.6.0: CI/CD GitHub Actions
- v1.0.0: Walking skeleton complet

---

## [v0.4.0] - 2025-12-09

### Ajouté
- Webhook Stripe pour événement `checkout.session.completed`
- Modèle `Order` avec champs : `product`, `stripe_session_id`, `email`, `amount`, `status`, `download_token`, `download_count`
- Vue `/webhook/` avec vérification signature Stripe (`STRIPE_WEBHOOK_SECRET`)
- Vue `/download/<token>/` pour téléchargement sécurisé par token unique
- Compteur de téléchargements incrémental par Order
- Fallback création Order dans `/thanks/` si webhook non reçu (environnement local)
- Logging détaillé événements webhook (succès/erreurs)
- Template `download.html` pour page de téléchargement
- Configuration `STRIPE_WEBHOOK_SECRET` dans `.env`

### Modifié
- Template `thanks.html` : affichage conditionnel lien téléchargement si Order existe
- Vue `thanks()` : récupération Order existant ou création via fallback
- Migration 0004 : ajout modèle Order

### Sécurité
- Vérification signature webhook Stripe (protection CSRF exemptée car signature suffit)
- Protection doublons Orders (vérification `stripe_session_id` unique)
- Token téléchargement généré via `secrets.token_urlsafe(48)` (64 caractères)

### Tests
- Tests manuels validés en local (Nexus) avec fallback Order
- Tests webhook en attente déploiement production VPS

**Commit:** `feat(stripe): implement webhooks and secure download system`
**Tag:** `v0.4.0`

---

## [v0.3.0] - 2025-12-08

### Ajouté
- Intégration Stripe Checkout (SDK Python `stripe`)
- Vue `/checkout/<slug>/` pour création Stripe Checkout Session
- Redirection vers page hosted Stripe (`checkout.stripe.com`)
- Vue `/thanks/` pour confirmation paiement avec `session_id`
- Gestion erreurs Stripe (session expirée, invalide, carte refusée)
- Configuration dynamique URLs `success_url` et `cancel_url` (dev/prod compatible)
- Variables environnement : `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- Documentation complète : `docs/STRIPE_SETUP.md`

### Modifié
- Template `product.html` : bouton "Acheter maintenant" POST vers `/checkout/`
- Template `thanks.html` : affichage statut paiement et détails session

### Sécurité
- Protection CSRF sur formulaire checkout
- Prix récupéré depuis base de données (non modifiable côté client)
- Clés Stripe test mode (`pk_test_`, `sk_test_`)

**Commit:** `feat(stripe): Implémentation commandes Stripe`
**Tag:** Non créé (à créer)

---

## [v0.2.1] - 2025-11-XX

### Modifié
- Rebrand complet : "Pyxalix" → "Pyx"
- Domaines : `pyxalix.devamalix.fr` → `pyx.devamalix.fr`, `dm.nexus.local` → `pyx.nexus.local`
- Containers : `pyxalix_web` → `pyx_web`, `pyxalix_postgres` → `pyx_postgres`
- Network : `pyxalix-network` → `pyx-network`
- Templates HTML : remplacement "Pyxalix" → "Pyx" (5 fichiers)
- Documentation : mise à jour nomenclature (17 fichiers)

### Breaking Changes
- Nécessite mise à jour DNS OVH (`pyx.devamalix.fr`)
- Nécessite modification manuelle `.env` en production
- Nécessite redémarrage containers avec nouveaux noms

**Commit:** `refactor(brand): Rebrand Pyxalix → Pyx`
**Tag:** Non créé (à créer)

---

## [v0.2.0] - 2025-10-30

### Ajouté
- Template `base.html` avec Tailwind CSS (CDN)
- Design moderne et responsive : `catalog.html`, `product.html`, `thanks.html`
- Branding "Pyxalix" (couleurs indigo, header/footer)
- Vues `purchase()` et `thanks()` (mock payment temporaire)
- Service `nginx-static` mutualisé pour media files (performance x100)
- Architecture 3 environnements : `docker-compose.dev.yml`, `docker-compose.nexus.yml`, `docker-compose.yml` (prod)
- Traefik routing avec priorités (nginx priority 100, Django priority 1)
- Migration 0003 : chargement initial 3 produits (fixtures intégrées)
- Images produits noms fixes (pas de hash Django)
- Configuration `CSRF_TRUSTED_ORIGINS` pour HTTPS production
- Documentation infrastructure : `DOCKER-COMPOSE-CONFIGS.md`, `INFRASTRUCTURE.md`

### Modifié
- Routing Traefik : exclusion `/media/` du router Django
- Suppression volume `media_data` (nginx sert fichiers directement)

### Corrigé
- Media files 404 en production (nginx sert au lieu de Django)
- CSRF 403 en HTTPS sur VPS (trusted origins configurés)

### Supprimé
- Script `seed.py` (remplacé par migration 0003)
- 7 scripts obsolètes Windows PowerShell (bootstrap/audit)

**Tag:** `v0.2.0`

---

## [v0.1.2] - 2025-10-30

### Ajouté
- Fixtures Django : `core/fixtures/initial_data.json` (3 produits test)
- Migration 0003 : chargement automatique fixtures

### Modifié
- Variables environnement : passage `env_file` → interpolation `${VAR}` dans docker-compose
- Fichier `.env.docker` renommé → `.env` (convention Docker Compose)
- README : documentation environnements local + Nexus

### Corrigé
- Healthcheck PostgreSQL : `pg_isready -d dm_db` (DB name spécifié)

**Tag:** `v0.1.2`

---

## [v0.1.1] - 2025-10-29

### Ajouté
- Dockerisation complète : PostgreSQL 16 + Django 5.2.6
- Docker Compose avec hot-reload (volume bind mount)
- Healthcheck PostgreSQL et Django
- Configuration `.env.docker.example`
- Script d'initialisation Linux/Nexus

**Tag:** `v0.1.1`

---

## [v0.1.0] - 2025-10-29

### Ajouté
- Modèle `Product` (name, description, price, slug, image)
- Vue `catalog_view()` : liste tous les produits
- Vue `product_view(slug)` : détail produit
- Templates : `catalog.html`, `product.html`
- Migration 0002 : création modèle Product

**Tag:** `v0.1.0`

---

## [v0.0.2] - 2025-10-28

### Ajouté
- Endpoint `/health` (healthcheck JSON)
- Page d'accueil `/home` (template HTML basique)
- Templates : `home.html`

**Tag:** `v0.0.2`

---

## [v0.0.1] - 2025-10-28

### Ajouté
- Repository initial créé
- Django 5.2.6 project `backend` + app `core`
- Configuration initiale : `settings.py`, `urls.py`
- Hello world endpoint fonctionnel

**Tag:** `v0.0.1`

---

## Légende

### Types de changements
- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements sur fonctionnalités existantes
- **Obsolète** : Fonctionnalités bientôt supprimées
- **Supprimé** : Fonctionnalités retirées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Correctifs de vulnérabilités

### Symboles priorité (pour versions futures)
- 🔴 Haute : Critique pour production
- 🟡 Moyenne : Important mais non bloquant
- 🟢 Basse : Nice to have

---

**Dernière mise à jour :** 2025-12-09
**Version actuelle :** v0.4.0
**Prochaine version :** v0.5.0 (Tests unitaires)
