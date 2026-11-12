# Configuration Docker Compose - Pyx (DM)

**Date:** 28 octobre 2025
**Version:** 1.1 (mise à jour le 12 novembre 2026 : retrait de la configuration Nexus)

---

## Vue d'ensemble

Pyx utilise **2 fichiers docker-compose** pour gérer les environnements :

```
dm/
├── docker-compose.dev.yml     (Dev PC, pas de Traefik)
└── docker-compose.yml         (Prod VPS, Traefik HTTPS)
```

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

## 2. docker-compose.yml

**Usage :** Production VPS
**Commande :** `docker compose up -d` (fichier par défaut)

### Caractéristiques

- **Network :**
  - Interne : `pyx-network`
  - Externe : `traefik-network`
- **Ports exposés :** ❌ Non (Traefik only, sécurité)
- **Traefik :**
  - **Django :** `pyx.devamalix.fr` → port 8000
  - EntryPoint : `websecure` (HTTPS:443)
  - TLS : `certresolver=letsencrypt` (auto-certificat)
  - Router : `pyx-web`
  - Watchtower : auto-update activé
- **DEBUG :** 0 (désactivé)
- **Containers :** `pyx_web`, `pyx_postgres`
- **Volumes :** `postgres_data`, `media_data`

### Quand l'utiliser

- Production sur VPS
- Déploiement final avec HTTPS
- Mode sécurisé (pas de ports exposés)

---

## Workflow de déploiement

```
PC dev
    ↓
  docker-compose.dev.yml
    ↓ (branche, PR, merge)
VPS (main)
    ↓
  docker-compose.yml  ← Production
```

La production suit `main` : aucune modification directe dans `~/dm`.

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

### VPS (prod)

```bash
# SSH vers VPS
ssh ubuntu@37.59.115.242

# Aller dans le projet
cd ~/dm

# Mettre à jour (après fusion de la PR sur main)
git pull --ff-only

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
| **yml** (défaut) | VPS (prod) | pyx.devamalix.fr | ✅ | ❌ Traefik | 0 | Production |

---

## Variables d'environnement (.env)

### Exemple .env pour dev

```env
# Django
DJANGO_SECRET_KEY=dev-secret-key-change-in-prod
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

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
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,pyx.devamalix.fr

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

### Traefik ne détecte pas Django (VPS)

```bash
# Vérifier que traefik-network existe
docker network ls | grep traefik

# Vérifier labels
docker inspect pyx_web | grep traefik

# Voir logs Traefik
docker logs traefik 2>&1 | grep pyx
```

### Erreur 400 Bad Request (DisallowedHost)

```bash
# Vérifier ALLOWED_HOSTS dans .env
cat .env | grep ALLOWED_HOSTS

# Ajouter le domain manquant (VPS : pyx.devamalix.fr)

# Redémarrer
docker compose restart web
```

### Certificat SSL non généré (VPS)

```bash
# Vérifier DNS
nslookup pyx.devamalix.fr
# Doit répondre à l'IP du VPS

# Voir logs Traefik
docker logs traefik 2>&1 | grep -i acme

# Attendre 1-2 minutes pour génération auto
```

### Migrations non appliquées

```bash
# Voir état migrations
docker compose exec web python manage.py showmigrations

# Appliquer migrations
docker compose exec web python manage.py migrate

# Si problème: reset DB (DEV UNIQUEMENT)
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
```

---

## Checklist avant déploiement VPS

- [ ] .env configuré avec SECRET_KEY forte
- [ ] DEBUG=0 dans .env VPS
- [ ] ALLOWED_HOSTS contient pyx.devamalix.fr
- [ ] DB_PASSWORD fort et unique
- [ ] DNS pyx.devamalix.fr → IP du VPS configuré
- [ ] Traefik actif sur VPS
- [ ] Testé en local avec docker-compose.dev.yml
- [ ] Pas de .env dans Git (.gitignore vérifié)

---

**Auteur :** MatthALXdev
**Dernière mise à jour :** 12 novembre 2026
**Version Pyxalix :** v0.2.0
