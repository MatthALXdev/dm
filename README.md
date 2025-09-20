# DM — Digital Wallpapers Boutique

> Projet e-commerce minimaliste pour la vente de packs de fonds d’écran numériques.  
> Développé en Django 5, avec une approche **Walking Skeleton → MVP → Portfolio-ready**.

---

## 🎯 Objectifs du projet

- Créer une boutique numérique sécurisée et minimaliste.
- Mettre en place un **Walking Skeleton** (chaîne complète du front jusqu’au paiement).
- Faire évoluer par **sprints** : intégration Stripe, stockage Backblaze B2, emails transactionnels, sécurité production.
- Livrer un produit final prêt à être présenté dans un **portfolio** professionnel.

---

## 🛠️ Stack technique

- **Backend & Front** : Django 5 (SSR)
- **Base de données** : PostgreSQL (prod), SQLite (dev)
- **Paiement** : Stripe Checkout
- **Stockage** : Backblaze B2 (fichiers protégés par URL presignées)
- **Emails** : Postmark / AWS SES
- **Infra** : VPS Hetzner + Nginx + systemd
- **Sécurité & Réseau** : Cloudflare (DNS/CDN/WAF, TLS)

---

## 🚀 Installation rapide (dev)

1. Cloner le repo et entrer dans le dossier :

   ```bash
   git clone git@github.com:VOTRE_USER/dm.git
   cd dm

   ```

2. Créer et activer un environnement virtuel :

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate # Windows
   source .venv/bin/activate # Linux/Mac

   ```

3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Appliquer les migrations :

   ```bash
   python manage.py migrate
   ```

5. Lancer le serveur de développement :

   ```bash
   python manage.py runserver
   ```

6. Accéder à l'application :
   - Frontend : http://127.0.0.1:8000
   - Backend : http://127.0.0.1:8000/admin

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

---

## 👤 Auteur

Projet développé dans le cadre d’un **portfolio personnel** pour démontrer :

- L’approche de développement **incrémentale & sécurisée**
- L’utilisation d’**IA comme copilote**
- La mise en place d’une **stack moderne de e-commerce digital**
