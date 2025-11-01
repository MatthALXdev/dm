# Checklist Déploiement VPS - Pyxalix v0.2.0

**Date:** 28 octobre 2025
**Objectif:** Déployer Pyxalix UI moderne sur VPS avec Traefik + HTTPS
**Durée estimée:** 1h - 1h30 (Traefik déjà actif sur VPS)

---

## Contexte

**Statut actuel:**
- ✅ UI Tailwind complète (v0.2.0) - testé sur Nexus
- ✅ Infrastructure Traefik **déjà opérationnelle sur VPS** (prod ReContent)
- ✅ **3 fichiers docker-compose créés** (dev.yml, nexus.yml, yml prod)
- ✅ **Testé sur Nexus** avec docker-compose.nexus.yml
- ✅ Documentation DOCKER-COMPOSE-CONFIGS.md créée
- ❌ Pas encore de tag GitHub v0.2.0
- ❌ DM (Pyxalix) pas encore cloné sur VPS

**Architecture existante VPS:**
```
VPS (37.59.115.242)
├── traefik/ (actif, gère recontent.devamalix.fr)
└── recontent/ (déployé avec HTTPS)

À ajouter : dm/ → pyx.devamalix.fr
```

**Architecture Nexus (référence):**
```
Nexus (192.168.1.22)
├── shared/traefik/ (notre modèle)
├── dev-web/dm/ (avec labels Traefik prêts)
└── dev-web/recontent/ (config docker-compose.nexus.yml)
```

---

## Phase 1 : Préparation Git (15 min)

### 1.1 Vérifier l'état du code

```bash
cd /home/matth/nexus/dev-web/dm
git status
git log --oneline -5
```

**Vérifier:**
- [ ] Toutes les modifs UI sont committées
- [ ] Branch actuelle = `develop` ou `main`
- [ ] Aucun fichier .env ou secrets en staging

### 1.2 Créer le tag v0.2.0

```bash
git tag -a v0.2.0 -m "feat: Modern UI with Tailwind CSS

- Refonte complète catalog/product/thanks
- Design responsive et professionnel
- Branding Pyxalix (indigo)
- Mock payment flow complet"

git push origin v0.2.0
```

**Vérifier sur GitHub:**
- [ ] Tag visible dans l'onglet "Releases"

### 1.3 Vérifier .gitignore

```bash
cat .gitignore | grep -E "(\.env|__pycache__|db\.sqlite3)"
```

**Doit contenir:**
```
.env
.env.local
__pycache__/
*.pyc
db.sqlite3
media/
```

---

## Phase 2 : Vérification config (DÉJÀ FAIT)

**✅ 3 fichiers docker-compose créés et testés :**

- `docker-compose.dev.yml` → Dev PC sans Traefik
- `docker-compose.nexus.yml` → Test Nexus HTTP
- `docker-compose.yml` → **Prod VPS HTTPS** (prêt à deploy)

**✅ Testé sur Nexus :** `http://pyx.nexus.local/catalog/` fonctionne

**Différences principales Nexus ↔ VPS :**

| Config | docker-compose.nexus.yml | docker-compose.yml (VPS) |
|--------|--------------------------|--------------------------|
| Domain | `pyx.nexus.local` | `pyx.devamalix.fr` |
| EntryPoint | `web` (HTTP) | `websecure` (HTTPS) |
| TLS | ❌ Non | ✅ `letsencrypt` |
| Ports exposés | ✅ 8000, 5432 (debug) | ❌ Non (sécurité) |
| Containers | `dm_web`, `dm_postgres` | `pyx_web`, `pyx_postgres` |
| Network | `nexus-dm` | `pyx-network` |

**📖 Documentation :** [DOCKER-COMPOSE-CONFIGS.md](../DOCKER-COMPOSE-CONFIGS.md)

---

## Phase 3 : Configuration DNS (10 min)

### 3.1 Créer le sous-domaine

**Se connecter sur OVH:** https://www.ovh.com/manager/

1. Aller dans "Domaines" → `devamalix.fr`
2. Onglet "Zone DNS"
3. Cliquer "Ajouter une entrée"
4. Type : **A**
5. Sous-domaine : **pyxalix**
6. Cible : **37.59.115.242** (IP VPS)
7. Sauvegarder

### 3.2 Vérifier la propagation DNS

**Attendre 2-5 minutes, puis tester:**

```bash
ping pyx.devamalix.fr
# Doit répondre avec 37.59.115.242
```

**Alternative (si ping bloqué):**

```bash
nslookup pyx.devamalix.fr
# Doit afficher Address: 37.59.115.242
```

---

## Phase 4 : Test final sur Nexus (VALIDÉ ✅)

**✅ Tests effectués avec docker-compose.nexus.yml :**

- [x] Page catalog s'affiche avec UI Tailwind
- [x] Container dm_web healthy
- [x] Routing Traefik `pyx.nexus.local` → Django OK
- [x] 3 produits chargés via seed data

**URL testée :** `http://pyx.nexus.local/catalog/` → Fonctionne

**→ Configuration validée, prête pour VPS**

---

## Phase 5 : Déploiement VPS (30 min)

### 5.1 Connexion SSH

```bash
ssh ubuntu@37.59.115.242
# Ou si alias configuré :
ssh vps-devamalix
```

### 5.2 Cloner le projet

**DM n'existe pas encore sur VPS (premier déploiement):**

```bash
cd ~
git clone https://github.com/MatthALXdev/dm.git
cd dm
```

**Vérifier la branche:**

```bash
git branch
# Doit afficher * main
```

### 5.3 Configuration .env

**Créer/éditer le fichier .env:**

```bash
cp .env.example .env
nano .env
```

**Contenu minimal:**

```env
# Django
DJANGO_SECRET_KEY=<GENERER-UNE-CLE-ALEATOIRE>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,pyx.devamalix.fr

# Database
DB_NAME=dm_db
DB_USER=dm_user
DB_PASSWORD=<MOT-DE-PASSE-FORT>
DB_HOST=db
DB_PORT=5432

# Stripe (optionnel pour v0.2.0)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

**Générer SECRET_KEY Django:**

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Sauvegarder:** `Ctrl+O` puis `Ctrl+X`

### 5.4 Vérifier Traefik actif sur VPS

```bash
docker ps | grep traefik
# Doit afficher le container traefik actif
```

**Traefik est normalement déjà actif** (gère recontent.devamalix.fr).

**Si besoin de restart :**

```bash
cd ~/traefik
docker compose restart
```

### 5.6 Lancer Pyxalix

```bash
cd ~/dm
docker compose up -d --build
```

**Observer les logs:**

```bash
docker compose logs -f
# Ctrl+C pour sortir après 30s
```

**Vérifier que les containers sont UP:**

```bash
docker compose ps
```

**Attendu:**
```
dm_web       Up (healthy)
dm_postgres  Up (healthy)
```

### 5.7 Appliquer les migrations

```bash
docker compose exec web python manage.py migrate
```

### 5.8 Charger les données de test

```bash
docker compose exec web python manage.py loaddata initial_data
```

**Si fichier initial_data n'existe pas :**

Créer des produits manuellement via shell :

```bash
docker compose exec web python manage.py shell

# Dans le shell Python :
from core.models import Product
Product.objects.create(
    name="Pack Abstract",
    slug="pack-abstract",
    price=19.99,
    description="10 fonds d'écran abstraits"
)
# Ctrl+D pour sortir
```

---

## Phase 6 : Validation (15 min)

### 6.1 Vérifier certificat SSL

**Ouvrir navigateur:** `https://pyx.devamalix.fr`

**Vérifier:**
- [ ] Redirection HTTP → HTTPS automatique
- [ ] Cadenas vert (certificat valide)
- [ ] Certificat émis par "Let's Encrypt"

**Voir détails certificat:** Clic sur cadenas → "Certificat valide"

### 6.2 Tester le parcours complet

1. **Catalog:** `https://pyx.devamalix.fr/catalog/`
   - [ ] Page s'affiche avec UI Tailwind
   - [ ] Grid responsive visible
   - [ ] Produits chargés

2. **Product:** Cliquer sur un produit
   - [ ] URL type `/product/pack-abstract/`
   - [ ] Détails produit affichés
   - [ ] Bouton "Acheter maintenant" visible

3. **Purchase → Thanks:** Cliquer sur "Acheter maintenant"
   - [ ] Redirection vers `/thanks/pack-abstract/`
   - [ ] Message "Merci pour votre achat !"
   - [ ] Récapitulatif commande affiché

4. **Retour catalog:** Cliquer sur "Retour au catalogue"
   - [ ] Retour sur `/catalog/`

### 6.3 Tests responsive

**Ouvrir DevTools (F12) → Mode responsive:**

- [ ] Mobile (375px) : 1 colonne
- [ ] Tablet (768px) : 2 colonnes
- [ ] Desktop (1024px) : 3 colonnes

### 6.4 Vérifier logs Traefik (debug)

**Dashboard Traefik:** `https://traefik.devamalix.fr` (si configuré)

**Ou via logs:**

```bash
cd ~/traefik
docker compose logs | grep pyxalix
```

**Vérifier:**
- [ ] Router `pyx-web` actif
- [ ] Certificat généré automatiquement
- [ ] Pas d'erreur 502/504

### 6.5 Test mobile réel (bonus)

**Générer QR code:** https://www.qr-code-generator.com/

- URL : `https://pyx.devamalix.fr/catalog/`
- Scanner avec smartphone
- [ ] Page s'affiche correctement
- [ ] Responsive fonctionne

---

## Phase 7 : Documentation (10 min)

### 7.1 Mettre à jour README.md

**Ajouter section démo:**

```markdown
## Demo Live

🔗 **https://pyx.devamalix.fr**

Version actuelle : v0.2.0 (UI moderne avec Tailwind CSS)
```

### 7.2 Screenshot du résultat

**Prendre 3 captures d'écran:**

1. Page catalog (grid produits)
2. Page product (détail)
3. Page thanks (confirmation)

**Sauvegarder dans:** `docs/screenshots/v0.2.0/`

### 7.3 Commit final

```bash
git add README.md docs/screenshots/
git commit -m "docs: Add live demo link and screenshots v0.2.0"
git push origin main
```

---

## Checklist finale

### Fonctionnel
- [ ] `https://pyx.devamalix.fr` accessible
- [ ] Certificat SSL valide (HTTPS)
- [ ] UI Tailwind affichée correctement
- [ ] Parcours complet : catalog → product → purchase → thanks
- [ ] Responsive mobile/tablet/desktop
- [ ] Produits de test chargés

### Technique
- [ ] Tag GitHub v0.2.0 créé
- [ ] DNS `pyx.devamalix.fr` → `37.59.115.242`
- [ ] Traefik route correctement vers dm_web
- [ ] Containers healthy (web + postgres)
- [ ] .env configuré et sécurisé (pas committé)
- [ ] README.md mis à jour avec lien démo

### Sécurité
- [ ] DEBUG=0 en prod
- [ ] SECRET_KEY unique et fort
- [ ] DB_PASSWORD fort
- [ ] .env dans .gitignore
- [ ] Pas de secrets dans Git

---

## Troubleshooting

### Erreur 502 Bad Gateway

**Cause possible:** Container web pas démarré ou crashé

**Solution:**
```bash
docker compose logs web
docker compose restart web
```

### Erreur 400 Bad Request (DisallowedHost)

**Cause:** ALLOWED_HOSTS pas configuré

**Solution:**
```bash
# Dans .env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,pyx.devamalix.fr
docker compose restart web
```

### Certificat SSL non généré

**Cause:** DNS pas propagé ou Traefik pas actif

**Solution:**
```bash
# Vérifier DNS
nslookup pyx.devamalix.fr

# Vérifier Traefik
cd ~/traefik
docker compose logs | grep letsencrypt

# Forcer renouvellement
docker compose restart
```

### Page blanche / 404

**Cause:** Static files ou migrations manquantes

**Solution:**
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose restart web
```

---

## Prochaines étapes (après validation)

**v0.3.0 (prévu) :**
- Intégration Stripe Checkout réel
- Modèle Order
- Paiement fonctionnel

**Préparation entretien :**
- QR code Pyxalix pour démo mobile
- Préparer pitch 30s projet
- Screenshots haute qualité
- Lister défis techniques résolus

---

**Dernière mise à jour:** 28 octobre 2025
**Version cible:** v0.2.0
**Status:** ⏳ En attente déploiement VPS
