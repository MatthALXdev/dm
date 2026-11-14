# Configuration Stripe - Guide complet

## 📋 Vue d'ensemble

Ce guide explique comment configurer Stripe Checkout pour le projet Pyx (Digital Marketplace).

**Version :** v0.4.0
**Type d'intégration :** Stripe Checkout + Webhooks
**Mode actuel :** Test mode
**Dernière MAJ :** 8 décembre 2025

---

## 🔑 Obtenir les clés API Stripe

### 1. Créer un compte Stripe

1. Aller sur [https://dashboard.stripe.com/register](https://dashboard.stripe.com/register)
2. Créer un compte (email + mot de passe)
3. Vérifier l'email

### 2. Récupérer les clés de test

1. Se connecter au [Dashboard Stripe](https://dashboard.stripe.com/)
2. Cliquer sur **Developers** (menu gauche)
3. Cliquer sur **API keys**
4. Copier les clés suivantes :
   - **Publishable key** (commence par `pk_test_`)
   - **Secret key** (commence par `sk_test_`) - cliquer sur "Reveal test key"

### 3. Ajouter les clés dans `.env`

```bash
# Configuration Stripe (v0.4.0+)
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE
STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_CLE_WEBHOOK  # Généré via Stripe CLI ou Dashboard
```

⚠️ **IMPORTANT :** Ne jamais commit le fichier `.env` sur Git !

---

## 🏗️ Architecture de l'intégration

### Flux utilisateur (v0.4.0+)

```
1. Utilisateur clique "Acheter maintenant" sur /product/<slug>/
   ↓
2. POST vers /checkout/<slug>/
   ↓
3. Django crée une Stripe Checkout Session (avec metadata product_id)
   ↓
4. Redirection vers Stripe hosted checkout page (https://checkout.stripe.com/...)
   ↓
5. Utilisateur entre ses informations de carte
   ↓
6. Paiement réussi → Redirection vers /thanks/?session_id=cs_xxx
   ↓                    ↓
   ↓                    Stripe envoie webhook checkout.session.completed
   ↓                    ↓
   ↓                    Django crée Order + token téléchargement
   ↓
7. Page /thanks/ affiche confirmation + lien téléchargement
   ↓
8. Utilisateur clique sur "Télécharger" → /download/<token>/
   ↓
9. Django vérifie token et affiche page téléchargement
```

### Composants techniques (v0.4.0)

| Composant | Fichier | Description |
|-----------|---------|-------------|
| **Modèle Order** | `core/models.py:20-47` | Stocke commandes + token téléchargement |
| **Vue checkout** | `core/views.py:39-73` | Crée Stripe Checkout Session + metadata |
| **Vue thanks** | `core/views.py:82-122` | Affiche confirmation + lien download si Order existe |
| **Vue webhook** | `core/views.py:125-144` | Vérifie signature + crée Order |
| **Vue download** | `core/views.py:181-205` | Vérifie token + affiche page téléchargement |
| **Template product** | `core/templates/core/product.html:26` | Bouton POST /checkout/ |
| **Template thanks** | `core/templates/core/thanks.html:45-66` | Bouton download conditionnel |
| **Template download** | `core/templates/core/download.html` | Page téléchargement avec infos order |
| **Configuration** | `backend/settings.py:84-87` | Clés API Stripe |
| **Tests** | `core/test_stripe.py` | Tests automatisés (19 tests) |

### Construction dynamique des URLs (v0.3.1+)

Les URLs de redirection sont construites dynamiquement pour supporter dev et prod :

```python
# core/views.py:43-44
base_url = f"{request.scheme}://{request.get_host()}"
success_url = f'{base_url}/thanks/?session_id={{CHECKOUT_SESSION_ID}}'
```

**Environnements supportés :**
- Dev local : `http://localhost:8000/`
- Production : `https://pyx.devamalix.fr/`

**Pourquoi pas `request.build_absolute_uri()` ?**
Cette fonction encode les accolades `{}` en `%7B%7D`, empêchant Stripe de reconnaître le placeholder `{CHECKOUT_SESSION_ID}`.

### Gestion des erreurs (v0.3.1+)

La vue `/thanks/` gère plusieurs cas d'erreur :

| Erreur | Comportement | Message utilisateur |
|--------|--------------|---------------------|
| Session manquante | Redirection `/catalog/` | "Aucune session de paiement trouvée" |
| Session expirée (>24h) | Redirection `/catalog/` | "Session expirée, recommencez" |
| Session invalide | Redirection `/catalog/` | "Session invalide ou expirée" |
| Erreur Stripe | Redirection `/catalog/` | "Erreur lors de la récupération" |

Les erreurs sont loggées dans les logs Django pour debug.

### Webhooks Stripe (v0.4.0+)

Le webhook `/webhook/` écoute l'événement `checkout.session.completed` pour créer automatiquement les Orders après paiement.

**Sécurité :**
- Vérification de la signature Stripe (`STRIPE_WEBHOOK_SECRET`)
- Protection contre les doublons (vérifie si Order existe déjà)
- Exemption CSRF (`@csrf_exempt`) car signature Stripe suffit

**Création Order :**
```python
Order.objects.create(
    product=product,                          # Depuis metadata.product_id
    stripe_session_id=session['id'],          # ID unique session
    email=session['customer_details']['email'],
    amount=session['amount_total'] / 100,     # Converti en EUR
    status='paid',                            # Paiement confirmé
    download_token=secrets.token_urlsafe(48)  # Auto-généré
)
```

**Logs webhook :**
- ✅ Succès : `Order #X créé: email@example.com - Product Name - Token: abc123...`
- ❌ Erreur : `Webhook: product_id manquant`, `Webhook: Product X introuvable`, etc.

### Token de téléchargement (v0.4.0+)

Chaque Order possède un `download_token` unique :
- Généré via `secrets.token_urlsafe(48)` (64 caractères)
- Unique dans la base de données (contrainte `unique=True`)
- Valable indéfiniment
- Permet accès à `/download/<token>/`

**Compteur de téléchargements :**
- `download_count` s'incrémente à chaque visite de `/download/<token>/`
- Pas de limite de téléchargements (peut être ajouté si besoin)

---

## 💳 Tester avec cartes de test Stripe

### Cartes valides (paiement réussi)

| Numéro | Description |
|--------|-------------|
| `4242 4242 4242 4242` | Visa - Paiement réussi |
| `5555 5555 5555 4444` | Mastercard - Paiement réussi |
| `3782 822463 10005` | American Express - Paiement réussi |

**Informations à renseigner :**
- **Date d'expiration :** N'importe quelle date future (ex: 12/25)
- **CVC :** N'importe quel code 3 chiffres (ex: 123)
- **Email :** N'importe quel email valide
- **Nom :** N'importe quel nom

### Cartes pour tester les erreurs

| Numéro | Résultat |
|--------|----------|
| `4000 0000 0000 0002` | Carte refusée (insufficient_funds) |
| `4000 0000 0000 9995` | Carte refusée (generic_decline) |
| `4000 0000 0000 0341` | Nécessite authentification 3D Secure |

Voir la [liste complète des cartes de test](https://stripe.com/docs/testing#cards).

---

## 🧪 Tester l'intégration localement

### 1. Démarrer les containers

```bash
docker compose -f docker-compose.dev.yml up -d
```

### 2. Accéder à l'application

```bash
# Ouvrir dans le navigateur
http://localhost:8000/catalog/
```

### 3. Parcours de test complet

1. Cliquer sur un produit (ex: "Aurores boréales")
2. Cliquer sur "Acheter maintenant"
3. Vérifier redirection vers `https://checkout.stripe.com/c/pay/cs_test_...`
4. Remplir le formulaire :
   - Email : `test@example.com`
   - Numéro de carte : `4242 4242 4242 4242`
   - Date : `12/25`
   - CVC : `123`
5. Cliquer "Pay"
6. Vérifier redirection vers `/thanks/?session_id=cs_test_...`
7. Vérifier affichage :
   - Montant total (ex: 5.99 EUR)
   - Statut du paiement : "Payé" (vert)
   - Email utilisé
   - Session ID

### 4. Vérifier dans Stripe Dashboard

1. Aller sur [https://dashboard.stripe.com/test/payments](https://dashboard.stripe.com/test/payments)
2. Voir le paiement test
3. Cliquer dessus pour voir les détails

---

## 🔐 Sécurité

### Variables sensibles

| Variable | Type | Exposition |
|----------|------|------------|
| `STRIPE_PUBLIC_KEY` | Publique | ✅ Peut être dans HTML/JS |
| `STRIPE_SECRET_KEY` | Secrète | 🔐 Serveur uniquement |
| `STRIPE_WEBHOOK_SECRET` | Secrète | 🔐 Serveur uniquement |

### Bonnes pratiques

✅ **À faire :**
- Utiliser test mode pour développement (`pk_test_`, `sk_test_`)
- Stocker clés dans `.env` (jamais hardcodé)
- Ajouter `.env` dans `.gitignore`
- Vérifier signature webhook (v0.4.0)

❌ **À éviter :**
- Commit clés Stripe sur Git
- Utiliser clés production (`pk_live_`, `sk_live_`) en dev
- Logger clés secrètes dans console/fichiers

---

## 🐛 Troubleshooting

### Erreur : "No such checkout session"

**Cause :** Session ID invalide ou expiré (24h max)

**Solution :**
- Refaire un achat complet
- Vérifier que `session_id` est bien passé dans l'URL

### Erreur : "Invalid API Key"

**Cause :** Clé Stripe incorrecte ou non chargée

**Solution :**
```bash
# Vérifier que les clés sont dans .env
cat .env | grep STRIPE

# Redémarrer le container pour recharger .env
docker restart dm_web
```

### Erreur : Redirection échoue après paiement

**Cause :** `success_url` mal configuré

**Solution :**
- Vérifier que la vue `thanks` ne nécessite pas le paramètre `slug`
- Vérifier la route : `path("thanks/", thanks, name="thanks")`

### Le paiement fonctionne mais aucune commande en DB

**Normal pour v0.3.0** → La création automatique d'Order sera implémentée en **v0.4.0** via webhook Stripe.

---

## 🧪 Tests automatisés (v0.4.0+)

### Lancer les tests

```bash
docker exec dm_web pytest core/test_stripe.py -v
```

### Tests implémentés (19 tests)

**Checkout (3 tests) :**
- ✅ Création session Stripe et redirection
- ✅ Slug invalide → 404
- ✅ GET au lieu de POST → redirection catalog

**Page Thanks (4 tests) :**
- ✅ Session valide → affiche données
- ✅ Sans session_id → redirige avec message
- ✅ Session expirée → redirige avec message
- ✅ Session invalide → redirige avec message

**Sécurité (4 tests) :**
- ✅ Protection injection SQL (slug)
- ✅ Protection XSS (product.name)
- ✅ Protection CSRF (POST checkout)
- ✅ Prix depuis DB (pas modifiable client)

**Webhooks (4 tests) :**
- ✅ Webhook crée Order après checkout.session.completed
- ✅ Signature invalide → 400
- ✅ Prévention doublons (même session_id)
- ✅ Metadata sans product_id → pas de création

**Téléchargement (4 tests) :**
- ✅ Token valide → affiche page téléchargement
- ✅ Compteur download_count s'incrémente
- ✅ Token invalide → redirige avec message
- ✅ Statut 'pending' (non payé) → refusé

### Résultats attendus

```
19 passed in 0.99s
```

---

## 🔒 Tests de sécurité (v0.3.1+)

| Vulnérabilité | Protection | Statut |
|---------------|------------|--------|
| **Injection SQL** | Django ORM (`get_object_or_404`) | ✅ Protégé |
| **XSS** | Échappement auto Django templates | ✅ Protégé |
| **CSRF** | `{% csrf_token %}` sur formulaires | ✅ Protégé |
| **Prix modifié** | Récupéré depuis DB serveur | ✅ Protégé |

### Tests manuels de sécurité

```bash
# 1. Test injection SQL
curl "http://localhost:8000/product/test'; DROP TABLE products;--/"
# Résultat attendu : 404 (pas d'erreur SQL)

# 2. Test XSS (créer produit avec script dans nom via admin Django)
# Résultat attendu : script échappé en &lt;script&gt;

# 3. Test CSRF (POST sans token)
# Résultat attendu : 403 Forbidden
```

---

## 🔗 Configuration Webhook Stripe (v0.4.0+)

### 1. Via Stripe CLI (Développement local)

**Installation Stripe CLI :**
```bash
# Linux/Mac
brew install stripe/stripe-cli/stripe

# Ou télécharger depuis https://stripe.com/docs/stripe-cli
```

**Rediriger webhooks en local :**
```bash
# Forward webhooks vers votre environnement local
stripe listen --forward-to http://localhost:8000/webhook/

# Copier le webhook signing secret affiché (commence par whsec_)
# L'ajouter dans .env comme STRIPE_WEBHOOK_SECRET
```

**Déclencher webhook de test :**
```bash
stripe trigger checkout.session.completed
```

### 2. Via Stripe Dashboard (Production)

1. Aller sur [Stripe Dashboard > Developers > Webhooks](https://dashboard.stripe.com/test/webhooks)
2. Cliquer **"Add endpoint"**
3. Renseigner :
   - **Endpoint URL :** `https://pyx.devamalix.fr/webhook/`
   - **Events to send :** Sélectionner `checkout.session.completed`
4. Cliquer **"Add endpoint"**
5. Copier le **Signing secret** (commence par `whsec_`)
6. L'ajouter dans `.env` du serveur production

### 3. Tester le webhook

```bash
# Voir les logs en temps réel
docker logs -f dm_web

# Faire un achat test
# Observer dans les logs :
# "Order #X créé: test@example.com - Product Name - Token: abc123..."
```

**Vérifier dans l'admin Django :**
```bash
# Accéder à l'admin
http://localhost:8000/admin/core/order/

# Vérifier que l'Order a été créé avec :
# - Email correct
# - Montant correct
# - Status = 'paid'
# - download_token rempli
```

---

## 📚 Prochaines étapes (v0.5.0)

- Email automatique après achat avec lien téléchargement
- Système de limitation téléchargements (ex: max 10 fois)
- Gestion des remboursements via webhook `charge.refunded`
- Dashboard utilisateur pour voir ses achats

---

## 🔗 Ressources officielles

- [Documentation Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Cartes de test Stripe](https://stripe.com/docs/testing)
- [Webhooks Stripe](https://stripe.com/docs/webhooks)
- [SDK Python Stripe](https://stripe.com/docs/api/python)

---

**Dernière mise à jour :** 8 décembre 2025
**Auteur :** Matthieu (Pyx Digital Marketplace)
**Version intégration :** v0.4.0 - Webhooks + Téléchargements
