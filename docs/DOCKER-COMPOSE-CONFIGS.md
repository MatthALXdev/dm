# Configuration Docker Compose - Pyxalix (DM)

**Date:** 28 octobre 2025
**Version:** 1.0

---

## Vue d'ensemble

Pyxalix utilise **3 fichiers docker-compose** pour gérer différents environnements :

```
dm/
├── docker-compose.dev.yml     (Dev PC, pas de Traefik)
├── docker-compose.nexus.yml   (Test Nexus, Traefik HTTP)
└── docker-compose.yml         (Prod VPS, Traefik HTTPS)
```

**🎯 Objectif :** Architecture cohérente avec ReContent, tests pré-prod avant déploiement VPS.

---

## 1. docker-compose.dev.yml

**Usage :** Développement rapide sur PC
**Commande :** `docker compose -f docker-compose.dev.yml up`

### Caractéristiques

- **Network :** Interne uniquement (`dm-dev-network`)
- **Ports exposés :**
  - Django : `8000:8000`
  - PostgreSQL : `5432:5432` (pour pgAdmin)
- **Traefik :** ❌ Pas de labels
- **DEBUG :** 1 (activé)
- **Containers :** `dm_web_dev`, `dm_postgres_dev`
- **Volumes :** `postgres_data_dev`, `media_data_dev`

### Quand l'utiliser

- Développement rapide sur PC personnel
- Tests sans infrastructure Traefik
- Itérations rapides (hot reload Django)
- Accès direct via `http://localhost:8000`
- Connexion DB externe (DBeaver, pgAdmin)

---

## 2. docker-compose.nexus.yml

**Usage :** Test local avec Traefik HTTP
**Commande :** `docker compose -f docker-compose.nexus.yml up -d`

**📅 Créé le :** 28 octobre 2025
**🎯 Objectif :** Reproduire l'architecture VPS en local pour tests pré-production

### Caractéristiques

- **Network :**
  - Interne : `nexus-dm`
  - Externe : `traefik-network` (partagé avec ReContent, etc.)
- **Ports exposés :**
  - Django : `8000:8000` (fallback accès direct)
  - PostgreSQL : `5432:5432` (optionnel, pour debug)
- **Traefik :**
  - **Django :** `dm.nexus.local` → port 8000
  - EntryPoint : `web` (HTTP, pas HTTPS)
  - Router : `dm-web-nexus`
- **DEBUG :** 1 (peut rester activé en test local)
- **Containers :** `dm_web`, `dm_postgres`
- **Volumes :** `postgres_data`, `media_data`

### Différences vs VPS

| Aspect | Nexus | VPS |
|--------|-------|-----|
| Domain | `dm.nexus.local` | `pyxalix.devamalix.fr` |
| EntryPoint | `web` (HTTP) | `websecure` (HTTPS) |
| TLS | ❌ Non | ✅ Let's Encrypt |
| Port 8000 exposé | ✅ Oui (fallback) | ❌ Non (sécurité) |
| Port 5432 exposé | ✅ Oui (debug DB) | ❌ Non (sécurité) |
| DEBUG | 1 | 0 |
| Containers | dm_web | pyxalix_web |
| Network | nexus-dm | pyxalix-network |

### Quand l'utiliser

- ✅ Tester config Traefik avant déploiement VPS
- ✅ Valider routing Django via Traefik
- ✅ Tester architecture identique à prod (sans HTTPS)
- ✅ Vérifier healthcheck PostgreSQL
- ❌ Pas pour dev rapide (utiliser docker-compose.dev.yml)

---

## 3. docker-compose.yml

**Usage :** Production VPS
**Commande :** `docker compose up -d` (fichier par défaut)

### Caractéristiques

- **Network :**
  - Interne : `pyxalix-network`
  - Externe : `traefik-network`
- **Ports exposés :** ❌ Non (Traefik only, sécurité)
- **Traefik :**
  - **Django :** `pyxalix.devamalix.fr` → port 8000
  - EntryPoint : `websecure` (HTTPS:443)
  - TLS : `certresolver=letsencrypt` (auto-certificat)
  - Router : `pyxalix-web`
  - Watchtower : auto-update activé
- **DEBUG :** 0 (désactivé)
- **Containers :** `pyxalix_web`, `pyxalix_postgres`
- **Volumes :** `postgres_data`, `media_data`

### Quand l'utiliser

- Production sur VPS (37.59.115.242)
- Déploiement final avec HTTPS
- Environnement clients réels
- Mode sécurisé (pas de ports exposés)

---

## Workflow de déploiement

```
PC dev (develop-extern)
    ↓
  docker-compose.dev.yml
    ↓ (git push)
Nexus (develop-home)
    ↓
  docker-compose.nexus.yml  ← Test pré-prod
    ↓ (git merge → main)
VPS (main)
    ↓
  docker-compose.yml  ← Production
```

---

## Commandes utiles

### Dev (PC)

```bash
# Démarrer en mode dev
docker compose -f docker-compose.dev.yml up

# Rebuild après changement code
docker compose -f docker-compose.dev.yml up --build

# Migrations
docker compose -f docker-compose.dev.yml exec web python manage.py migrate

# Créer superuser
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Arrêter
docker compose -f docker-compose.dev.yml down
```

### Nexus (test)

```bash
# SSH vers Nexus
ssh matth@nexus.local

# Aller dans le projet
cd /home/matth/nexus/dev-web/dm

# Pull dernières modifs
git pull origin develop-home

# Démarrer avec config Nexus
docker compose -f docker-compose.nexus.yml up -d --build

# Voir logs
docker compose -f docker-compose.nexus.yml logs -f web

# Migrations
docker compose -f docker-compose.nexus.yml exec web python manage.py migrate

# Arrêter
docker compose -f docker-compose.nexus.yml down
```

### VPS (prod)

```bash
# SSH vers VPS
ssh ubuntu@37.59.115.242

# Aller dans le projet
cd ~/dm

# Pull dernières modifs
git pull origin main

# Démarrer (utilise docker-compose.yml par défaut)
docker compose up -d --build

# Migrations
docker compose exec web python manage.py migrate

# Collecter static files
docker compose exec web python manage.py collectstatic --noinput

# Voir logs
docker compose logs -f web

# Arrêter
docker compose down
```

---

## Tableau récapitulatif

| Fichier | Environnement | Domain | HTTPS | Ports exposés | DEBUG | Utilisation |
|---------|---------------|--------|-------|---------------|-------|-------------|
| **dev.yml** | PC local | localhost | ❌ | ✅ 8000, 5432 | 1 | Dev rapide |
| **nexus.yml** | Nexus (test) | dm.nexus.local | ❌ | ✅ 8000, 5432 | 1 | Test pré-prod |
| **yml** (défaut) | VPS (prod) | pyxalix.devamalix.fr | ✅ | ❌ Traefik | 0 | Production |

---

## Migration d'une config à l'autre

### Nexus → VPS

Modifications nécessaires dans les labels Traefik :

```yaml
# AVANT (Nexus)
- "traefik.http.routers.dm-web-nexus.rule=Host(`dm.nexus.local`)"
- "traefik.http.routers.dm-web-nexus.entrypoints=web"
- "traefik.http.services.dm-web-nexus.loadbalancer.server.port=8000"

# APRÈS (VPS)
- "traefik.http.routers.pyxalix-web.rule=Host(`pyxalix.devamalix.fr`)"
- "traefik.http.routers.pyxalix-web.entrypoints=websecure"
- "traefik.http.routers.pyxalix-web.tls.certresolver=letsencrypt"
- "traefik.http.services.pyxalix-web.loadbalancer.server.port=8000"
```

**Noms des containers :**
```yaml
# Nexus
container_name: dm_web
container_name: dm_postgres

# VPS
container_name: pyxalix_web
container_name: pyxalix_postgres
```

**✅ Avec les 3 fichiers, plus besoin de modifier manuellement !**

---

## Variables d'environnement (.env)

### Exemple .env pour dev/nexus

```env
# Django
DJANGO_SECRET_KEY=dev-secret-key-change-in-prod
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.1.22,nexus.local,dm.nexus.local

# Database
DB_NAME=dm_db
DB_USER=dm_user
DB_PASSWORD=dev_password
DB_HOST=db
DB_PORT=5432

# Stripe (optionnel)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Exemple .env pour VPS

```env
# Django
DJANGO_SECRET_KEY=<GENERER-UNE-CLE-FORTE-ALEATOIRE>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,pyxalix.devamalix.fr

# Database
DB_NAME=dm_db
DB_USER=dm_user
DB_PASSWORD=<MOT-DE-PASSE-FORT-UNIQUE>
DB_HOST=db
DB_PORT=5432

# Stripe
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

**⚠️ IMPORTANT : Ne jamais commit .env dans Git !**

---

## Troubleshooting

### Port 8000 déjà utilisé (dev.yml)

```bash
# Vérifier quel process utilise le port
sudo lsof -i :8000

# Arrêter l'ancien container
docker compose -f docker-compose.dev.yml down
```

### Traefik ne détecte pas Django (nexus.yml)

```bash
# Vérifier que traefik-network existe
docker network ls | grep traefik

# Créer si manquant
docker network create traefik-network

# Vérifier labels
docker inspect dm_web | grep traefik

# Voir logs Traefik
cd /home/matth/nexus/shared/traefik
docker compose logs | grep dm
```

### Erreur 400 Bad Request (DisallowedHost)

```bash
# Vérifier ALLOWED_HOSTS dans .env
cat .env | grep ALLOWED_HOSTS

# Ajouter le domain manquant
# Pour Nexus: dm.nexus.local
# Pour VPS: pyxalix.devamalix.fr

# Redémarrer
docker compose restart web
```

### Certificat SSL non généré (VPS)

```bash
# Vérifier DNS
nslookup pyxalix.devamalix.fr
# Doit répondre 37.59.115.242

# Voir logs Traefik
cd ~/traefik
docker compose logs | grep letsencrypt

# Attendre 1-2 minutes pour génération auto
```

### Migrations non appliquées

```bash
# Voir état migrations
docker compose exec web python manage.py showmigrations

# Appliquer migrations
docker compose exec web python manage.py migrate

# Si problème: reset DB (DEV UNIQUEMENT)
docker compose down -v
docker compose up -d
docker compose exec web python manage.py migrate
```

---

## Checklist avant déploiement VPS

- [ ] .env configuré avec SECRET_KEY forte
- [ ] DEBUG=0 dans .env VPS
- [ ] ALLOWED_HOSTS contient pyxalix.devamalix.fr
- [ ] DB_PASSWORD fort et unique
- [ ] DNS pyxalix.devamalix.fr → 37.59.115.242 configuré
- [ ] Traefik actif sur VPS
- [ ] Testé sur Nexus avec docker-compose.nexus.yml
- [ ] Pas de .env dans Git (.gitignore vérifié)

---

**Auteur :** MatthALXdev
**Dernière mise à jour :** 28 octobre 2025
**Version Pyxalix :** v0.2.0
