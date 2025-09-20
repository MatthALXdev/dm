# CHECKLIST_ENV_DEVELOPPEMENT.md

> Objectif : verrouiller l’installation complète de l’environnement de développement **et** son évolution au fil des versions, puis esquisser un Sprint 3 ouvert visant un produit prêt à être présenté dans un portfolio.

---

## 1) Environnement de développement complet — Checklist d’installation (Verrouillée)

### 1.1 Prérequis (machine locale)
- [ ] OS : macOS / Windows / Linux (dev possible sur tous ; prod = Ubuntu sur VPS)
- [ ] Gestionnaire de paquets installé (Homebrew/winget/apt)
- [ ] Git installé et configuré (`git config --global user.name/user.email`)
- [ ] Clés SSH générées et ajoutées à l’hébergeur Git (GitHub/GitLab)
- [ ] Éditeur : VS Code (extension Python, Black, isort, EditorConfig)

### 1.2 Outils Python
- [ ] Python **3.12** installé
- [ ] `pip`, `venv` disponibles
- [ ] Environnement virtuel créé : `python -m venv venv`
- [ ] Activation du venv (snippet shell si besoin)
- [ ] Mise à jour de base : `pip install -U pip wheel`

### 1.3 Dépendances du projet (base)
- [ ] `pip install django python-dotenv gunicorn psycopg[binary] stripe requests`
- [ ] (Tests) `pip install pytest pytest-django`
- [ ] Créer `requirements.txt` (ou utiliser `pip-tools`)

### 1.4 Paramètres & secrets locaux
- [ ] Créer `.env` (jamais versionné)
- [ ] Renseigner les clés suivantes (valeurs de dev autorisées) :
  - Django : `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=True`, `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`
  - DB (dev) : SQLite par défaut — **PostgreSQL seulement en prod**
  - Stripe (test) : `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
  - Email (sandbox) : hôte SMTP/user/pass, `DEFAULT_FROM_EMAIL`
  - B2 (dev/test) : `B2_KEY_ID`, `B2_APPLICATION_KEY`, `B2_BUCKET`

### 1.5 Outils CLI utiles (optionnels mais recommandés)
- [ ] Stripe CLI (rediriger les webhooks en local)
- [ ] HTTPie ou curl (tester `/health`)
- [ ] pre-commit (`pip install pre-commit`) avec hooks : Black, isort, flake8

### 1.6 Bootstrap du projet
- [ ] `django-admin startproject dm .` (fait au Sprint 1)
- [ ] `python manage.py startapp core apps/core`
- [ ] `python manage.py migrate`
- [ ] `python manage.py runserver` → ouvrir http://127.0.0.1:8000/

### 1.7 Workflow Git (toujours actif)
- [ ] Repo initialisé ; `.gitignore` inclut `venv/`, `*.pyc`, `.env`, `/staticfiles/`
- [ ] Une branche par feature ; commits clairs
- [ ] Tag à chaque livrable (cf. docs VERSIONS)

---

## 2) Matrice d’évolution de l’environnement (par version)

> En local, on reste sur **SQLite** pour la rapidité tant qu’aucune requête spécifique PostgreSQL n’est requise. En production, on utilise **PostgreSQL** dès le déploiement Sprint 1.

| Version | Dépendances Outils Dev | Changements config | Notes |
|---|---|---|---|
| v0.0.1 | Django, dotenv | `.env` basique | Hello world seulement |
| v0.0.2 | — | Aucun | `/health`, home |
| v0.1.0 | — | Ajout migrations `Product` | SQLite OK |
| v0.2.0 | `stripe`, Stripe CLI (opt) | Clés Stripe test | Webhook forward local |
| v0.2.1 | — | Aucun | Message UI seulement |
| v0.3.0 | — | Secret webhook ; modèle Order | Logs paiements initiaux |
| v0.4.0 | — | Toggle téléchargement mock | Pas de stockage réel |
| v0.5.0 | SDK B2 (via `requests` ou lib) | Clés B2 dans `.env` | Bucket privé seulement |
| v0.6.0 | — | SMTP creds ; backend email | Sandbox d’abord |
| v0.7.0 | (Optionnel) outils CSS | — | SSR conservé ; pas de build frontend |
| v0.8.0 | — | Flags sécurité (env‑driven) | CSP en report-only |
| v0.9.0 | — | — | Infra prod seulement (VPS) |
| v1.0.0 | pytest/pytest-django | Module test settings | Smoke E2E via curl |
| v1.1.0 | — | Durcissement admin | Créer compte staff |
| v1.2.0 | — | Paramètres session panier | Cookies vérifiés |
| v1.3.x | — | Clés Stripe **live** (prod) | Idempotence & logs |
| v1.4.0 | — | TTL presign court | Liés aux commandes payées |
| v1.5.0 | — | Domaine email validé | DKIM/SPF/DMARC |
| v1.6.0 | — | — | Polissage UX |
| v1.7.0 | `argon2-cffi` | Validateurs mot de passe ; vérif email | Rate limiting |
| v1.8.0 | Agent monitoring (opt) | Seuils alertes | Échecs webhook/paiement |
| v2.0.0 | — | Versions figées | MVP livré |

---

## 3) Routines locales de run & test (raccourcis)
- Lancer serveur : `python manage.py runserver`
- Appliquer migrations : `python manage.py makemigrations && python manage.py migrate`
- Webhook Stripe (dev) : `stripe listen --forward-to localhost:8000/stripe/webhook`
- Lancer tests : `pytest -q`
- Linter/format : `black . && isort .`

---

## 4) Parité Prod — Différences minimales d’env
- DB : SQLite en dev ; Postgres en prod (migrations identiques)
- Secrets : `.env` local vs variables d’env sur serveur/CI
- Fichiers : Local → presign B2 test ; Prod → bucket privé réel
- Email : Local sandbox ; Prod domaine vérifié (SPF/DKIM/DMARC)
- Stripe : Local test ; Prod clés live + signature webhook
