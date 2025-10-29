# Infrastructure DM (Pyxalix)

Documentation de l'architecture et de l'infrastructure du projet DM.

## Architecture Globale

### Environnements

Le projet DM dispose de **3 environnements** avec **3 fichiers docker-compose** :

| Environnement | Fichier | Usage | DEBUG | Media Files |
|--------------|---------|-------|-------|-------------|
| **PC Dev** | `docker-compose.dev.yml` | Développement local rapide | ✅ | Django serve |
| **Nexus** | `docker-compose.nexus.yml` | Test pré-production | ❌ | nginx-static |
| **VPS** | `docker-compose.yml` | Production | ❌ | nginx-static |

### Stack Technique

```
┌─────────────────────────────────────────────────────────┐
│ Production (VPS) / Nexus (test)                         │
│                                                          │
│  Internet → Traefik (reverse proxy + HTTPS)            │
│              ↓                                           │
│              ├→ nginx-static → /media/products/*.png    │
│              │                                           │
│              └→ Django (Gunicorn à terme)               │
│                  ↓                                       │
│                  PostgreSQL 16                          │
└─────────────────────────────────────────────────────────┘
```

---

## Services

### 1. Django (web)

**Rôle** : Application backend Django

**Configuration** :
- Port interne : `8000`
- Serveur : `runserver` (dev), Gunicorn prévu pour prod
- Base de données : PostgreSQL 16
- Dépendances : `requirements.txt`

**Variables d'environnement** (`.env`) :
```bash
DJANGO_SECRET_KEY=<généré>
DJANGO_DEBUG=0  # 1 en dev, 0 en nexus/prod
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,pyxalix.devamalix.fr
DJANGO_CSRF_TRUSTED_ORIGINS=https://pyxalix.devamalix.fr

DB_NAME=dm_db
DB_USER=dm_user
DB_PASSWORD=<secret>
DB_HOST=db
DB_PORT=5432
```

**Migrations** :
```bash
# Appliquées automatiquement au démarrage via entrypoint.sh
python manage.py migrate

# Créer une nouvelle migration
docker compose exec web python manage.py makemigrations

# Voir l'état des migrations
docker compose exec web python manage.py showmigrations
```

---

### 2. PostgreSQL (db)

**Rôle** : Base de données relationnelle

**Configuration** :
- Image : `postgres:16-alpine`
- Port : `5432` (exposé uniquement sur Nexus pour debug)
- Volume : `postgres_data` (persistant)

**Healthcheck** : Vérifie que PostgreSQL est prêt avant de démarrer Django

**Backup** :
```bash
# Créer un backup
docker compose exec db pg_dump -U dm_user dm_db > backup.sql

# Restaurer un backup
docker compose exec -T db psql -U dm_user dm_db < backup.sql
```

---

## Fichiers Statiques et Media

### Stratégie

- **DEBUG=1 (dev)** : Django sert les media files via `urls.py`
- **DEBUG=0 (nexus/prod)** : nginx-static sert les media files

### Media Files

**Emplacement** : `media/products/`

**Images produits** :
- `forest_path.png` (Pack Nature)
- `ocean_waves.png` (Pack Abstract)
- `montain_sunset.png` (Pack Minimal)

**Important** : Les noms sont **fixes** (pas de hash Django) grâce à la migration de données `0003_load_initial_products.py`

### Configuration nginx

Les media files sont servis par `~/nexus/shared/nginx-static/` (mutualisé entre projets).

Voir `~/nexus/shared/nginx-static/README.md` pour la configuration.

---

## Données Initiales

### Migration vs Seed Script

❌ **Ancien système (supprimé)** : `seed.py`
- Créait les produits à chaque démarrage
- Ajoutait des hash aléatoires aux images
- Problème : doublons et incohérences

✅ **Nouveau système** : Migration de données `0003_load_initial_products.py`
- Exécutée **une seule fois** via `python manage.py migrate`
- Crée les 3 produits avec des chemins d'images fixes
- Utilise `get_or_create` pour éviter les doublons

### Produits Initiaux

| Nom | Slug | Prix | Image |
|-----|------|------|-------|
| Pack Nature | `pack-nature` | 9.99€ | `products/forest_path.png` |
| Pack Abstract | `pack-abstract` | 14.99€ | `products/ocean_waves.png` |
| Pack Minimal | `pack-minimal` | 19.99€ | `products/montain_sunset.png` |

---

## Routing Traefik

### Nexus (HTTP)

```yaml
labels:
  - "traefik.http.routers.dm-web-nexus.rule=Host(`dm.nexus.local`) && !PathPrefix(`/media/`)"
  - "traefik.http.routers.dm-web-nexus.entrypoints=web"
  - "traefik.http.routers.dm-web-nexus.priority=1"
```

**Exclusion `/media/`** : Les media files sont routés vers nginx-static (priorité 100)

### VPS (HTTPS)

```yaml
labels:
  - "traefik.http.routers.pyxalix-web.rule=Host(`pyxalix.devamalix.fr`) && !PathPrefix(`/media/`)"
  - "traefik.http.routers.pyxalix-web.entrypoints=websecure"
  - "traefik.http.routers.pyxalix-web.tls.certresolver=letsencrypt"
```

**Let's Encrypt** : Certificat SSL généré automatiquement par Traefik

---

## Déploiement

### 1. Sur PC (dev)

```bash
docker compose -f docker-compose.dev.yml up -d
# Accès : http://localhost:8000
```

### 2. Sur Nexus (test)

```bash
# Démarrer l'infra (Traefik + nginx-static)
cd ~/nexus/shared/traefik && docker compose up -d
cd ~/nexus/shared/nginx-static && docker compose up -d

# Démarrer DM
cd ~/nexus/dev-web/dm
docker compose -f docker-compose.nexus.yml up -d

# Accès : http://dm.nexus.local (via Traefik)
```

### 3. Sur VPS (production)

```bash
# Démarrer l'infra
cd ~/vps-infra/traefik && docker compose up -d
cd ~/vps-infra/nginx-static && docker compose up -d

# Préparer les media files
mkdir -p ~/dm/media/products
cp ~/dm/core/fixtures/img/*.png ~/dm/media/products/

# Configurer .env avec les vraies valeurs
nano ~/dm/.env

# Démarrer DM
cd ~/dm
docker compose build
docker compose up -d

# Accès : https://pyxalix.devamalix.fr
```

---

## Commandes Utiles

### Logs

```bash
# Logs Django
docker compose logs -f web

# Logs PostgreSQL
docker compose logs -f db

# Logs toutes les services
docker compose logs -f
```

### Shell Django

```bash
# Shell interactif
docker compose exec web python manage.py shell

# Créer un superuser
docker compose exec web python manage.py createsuperuser
```

### Base de données

```bash
# Accéder à PostgreSQL
docker compose exec db psql -U dm_user -d dm_db

# Reset complet de la base
docker compose down -v
docker compose up -d
```

### Rebuild

```bash
# Rebuild après changement Dockerfile/requirements.txt
docker compose build --no-cache
docker compose up -d
```

---

## Troubleshooting

### Images ne s'affichent pas

**Symptôme** : 404 sur `/media/products/*.png`

**Solutions** :
1. Vérifier que nginx-static tourne : `docker ps | grep nginx_static`
2. Vérifier que les images existent : `ls -la ~/nexus/dev-web/dm/media/products/`
3. Vérifier que Traefik route vers nginx : `curl -I http://dm.nexus.local/media/products/forest_path.png` → doit retourner `Server: nginx`

### CSRF errors en production

**Symptôme** : 403 Forbidden sur les POST

**Solution** : Vérifier que `DJANGO_CSRF_TRUSTED_ORIGINS` est défini dans `.env` :
```bash
DJANGO_CSRF_TRUSTED_ORIGINS=https://pyxalix.devamalix.fr
```

### Container redémarre en boucle

**Diagnostic** :
```bash
docker compose logs web
```

**Causes communes** :
- Base de données pas prête → healthcheck devrait gérer
- Erreur dans `.env` → vérifier les variables
- Erreur de migration → vérifier les logs

---

## Sécurité

### Production Checklist

- [ ] `DEBUG=False` dans `.env`
- [ ] `DJANGO_SECRET_KEY` généré avec `openssl rand -base64 50`
- [ ] `ALLOWED_HOSTS` configuré avec le bon domaine
- [ ] `CSRF_TRUSTED_ORIGINS` configuré pour HTTPS
- [ ] Mots de passe forts pour PostgreSQL
- [ ] Fichiers `.env` **jamais** committés dans Git
- [ ] HTTPS activé via Let's Encrypt
- [ ] Ports PostgreSQL **non exposés** en production

---

## Versions

- Python : 3.11
- Django : 5.2.6
- PostgreSQL : 16
- Traefik : 3.2
- nginx : alpine (latest)

---

## Références

- [DOCKER-COMPOSE-CONFIGS.md](./DOCKER-COMPOSE-CONFIGS.md) - Guide des 3 fichiers docker-compose
- [WORKFLOW-GIT-BRANCHES.md](../.claude/WORKFLOW-GIT-BRANCHES.md) - Workflow Git
- [README.md](../README.md) - Documentation générale du projet
- Infrastructure mutualisée : `~/nexus/shared/README.md`
