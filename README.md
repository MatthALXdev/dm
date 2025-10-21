# DM — Digital Wallpapers Boutique

> Projet e-commerce minimaliste pour la vente de packs de fonds d'écran numériques.  
> Développé en Django 5, avec une approche **Walking Skeleton → MVP → Portfolio-ready**.

---

## 🎯 Objectifs du projet

- Créer une boutique numérique sécurisée et minimaliste.
- Mettre en place un **Walking Skeleton** (chaîne complète du front jusqu'au paiement).
- Faire évoluer par **sprints** : intégration Stripe, stockage Backblaze B2, emails transactionnels, sécurité production.
- Livrer un produit final prêt à être présenté dans un **portfolio** professionnel.

---

## 🛠️ Stack technique

- **Backend & Front** : Django 5 (SSR)
- **Base de données** : PostgreSQL 16 (Docker)
- **Infrastructure** : Docker Compose (dev + prod)
- **Paiement** : Stripe Checkout
- **Stockage** : Backblaze B2 (fichiers protégés par URL presignées)
- **Emails** : Postmark / AWS SES
- **Infra** : VPS Hetzner + Nginx + systemd
- **Sécurité & Réseau** : Cloudflare (DNS/CDN/WAF, TLS)

---

## 🚀 Installation & Démarrage

### Prérequis

- Docker & Docker Compose
- Git

---

### 🏠 Environnement Local

1. **Cloner le repository**

   ```bash
   git clone https://github.com/MatthALXdev/dm.git
   cd dm
   ```

2. **Configurer les variables d'environnement**

   ```bash
   cp .env.example .env
   # Éditer .env avec vos valeurs locales
   ```

3. **Lancer l'application**

   ```bash
   docker compose up -d
   ```

4. **Charger les données de test**

   ```bash
   docker compose exec web python manage.py loaddata initial_data
   ```

5. **Créer un superuser (optionnel)**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

**Accès local :**
- 🌐 Application : http://localhost:8000
- 🔧 Admin Django : http://localhost:8000/admin
- 🗄️ PostgreSQL : localhost:5432

---

### 🖥️ Environnement Serveur (Nexus)

**Architecture actuelle**
- Serveur : Nexus (Ubuntu 22.04)
- Localisation : `~/nexus/dev-web/dm/`

**Accès serveur :**
- 🌐 Application : http://192.168.1.22:8000 ou http://nexus:8000
- 🔧 Admin Django : http://nexus:8000/admin
- 🗄️ PostgreSQL : 192.168.1.22:5432

**Commandes serveur**

```bash
# Connexion SSH
ssh nexus

# Navigation
cd ~/nexus/dev-web/dm

# Gestion des conteneurs
docker compose up -d        # Démarrer
docker compose down         # Arrêter
docker compose logs -f      # Voir les logs
docker compose restart      # Redémarrer

# Commandes Django
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata initial_data
docker compose exec web python manage.py createsuperuser
```

---

## 📂 Documentation

La documentation est organisée dans le dossier [`docs/`](./docs/).

- `progress/` → suivi des sprints (`S1E1.md`, `S1E2.md`…)
- `checklists/` → sécurité, installation, évolution env (`S1 security_checklist.md`, `cheklistInstall.md`…)
- `versions/` → suivi des livrables et temps (`S1 versions.md`, `S2 versions.md`)
- `roadmap/` → vision long terme (`S3 roadmap.md`)

Chaque sprint se termine par :

- Une revue de la checklist de sécurité
- Un tag Git versionné (cf. `docs/versions/`)

---

## 🗂️ Versions & Livrables

Le suivi des versions et livrables est consigné dans [`docs/versions/`](./docs/versions/).

**Versions récentes :**
- **v0.1.2** → Fixes configuration (interpolation env, fixtures, healthcheck)
- **v0.1.1** → Dockerisation complète (PostgreSQL + Django)
- **v0.1.0** → Structure projet initiale

Les principaux jalons :

- **Sprint 1** → Walking Skeleton sécurisé (Stripe test, webhook, B2 mock, email sandbox).
- **Sprint 2** → MVP e-commerce complet (paiement live, téléchargement réel, email prod).
- **Sprint 3** → Roadmap ouverte vers un produit portfolio-grade (UX, monitoring, polish).

---

## 🔐 Sécurité

Les règles de sécurité sont suivies par sprint dans [`docs/checklists/`](./docs/checklists/).

- **Sprint 1** → sécurité de base (HSTS, HTTPS, Cloudflare WAF, secrets en env).
- **Sprint 2** → durcissement (auth clients, Argon2, rate limiting, monitoring).
- **Sprint 3** → durcissement avancé (2FA admin, CSP strict, backups automatisés).

**Configuration actuelle :**
- Variables sensibles dans `.env` (non versionné)
- PostgreSQL isolé dans Docker network
- Fichier `.env.example` fourni comme template

---

## 🐳 Architecture Docker

**Services configurés :**

- **db** : PostgreSQL 16-alpine
  - Volume persistant `postgres_data`
  - Healthcheck avec `pg_isready -d dm_db`
  - Port 5432 exposé

- **web** : Django 5.2.6
  - Build depuis Dockerfile local
  - Hot-reload activé (volume monté)
  - Port 8000 exposé
  - Dépend du service `db` (healthcheck)

**Gestion des données :**
- Fixtures initiales : `core/fixtures/initial_data.json` (3 produits de test)
- Commande de chargement : `docker compose exec web python manage.py loaddata initial_data`

