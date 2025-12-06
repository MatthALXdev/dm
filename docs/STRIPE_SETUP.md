# Configuration Stripe - Guide complet

## 📋 Vue d'ensemble

Ce guide explique comment configurer Stripe Checkout pour le projet Pyx (Digital Marketplace).

**Version :** v0.3.0
**Type d'intégration :** Stripe Checkout (hosted page)
**Mode actuel :** Test mode

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
# Configuration Stripe (v0.3.0+)
STRIPE_PUBLIC_KEY=pk_test_VOTRE_CLE_PUBLIQUE
STRIPE_SECRET_KEY=sk_test_VOTRE_CLE_SECRETE
STRIPE_WEBHOOK_SECRET=whsec_placeholder_will_be_generated_in_v0.4.0
```

⚠️ **IMPORTANT :** Ne jamais commit le fichier `.env` sur Git !

---

## 🏗️ Architecture de l'intégration

### Flux utilisateur

```
1. Utilisateur clique "Acheter maintenant" sur /product/<slug>/
   ↓
2. POST vers /checkout/<slug>/
   ↓
3. Django crée une Stripe Checkout Session
   ↓
4. Redirection vers Stripe hosted checkout page (https://checkout.stripe.com/...)
   ↓
5. Utilisateur entre ses informations de carte
   ↓
6. Paiement réussi → Redirection vers /thanks/?session_id=cs_xxx
   ↓
7. Django récupère la session Stripe et affiche confirmation
```

### Composants techniques

| Composant | Fichier | Description |
|-----------|---------|-------------|
| **Modèle Order** | `core/models.py:19-38` | Stocke les commandes (v0.4.0 webhook) |
| **Vue checkout** | `core/views.py:36-68` | Crée Stripe Checkout Session |
| **Vue thanks** | `core/views.py:71-92` | Récupère session_id et affiche confirmation |
| **Template product** | `core/templates/core/product.html:26` | Bouton POST /checkout/ |
| **Template thanks** | `core/templates/core/thanks.html:19-43` | Affichage session Stripe |
| **Configuration** | `backend/settings.py:80-83` | Clés API Stripe |

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
cd /home/matth/nexus/dev-web/dm
docker compose -f docker-compose.nexus.yml up -d
```

### 2. Accéder à l'application

```bash
# Ouvrir dans le navigateur
http://dm.nexus.local/catalog/
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
cat /home/matth/nexus/dev-web/dm/.env | grep STRIPE

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

## 📚 Prochaines étapes (v0.4.0)

- Configurer webhook Stripe pour événement `checkout.session.completed`
- Créer endpoint `/webhook/stripe/` avec validation signature
- Automatiser création Order en DB après paiement validé
- Ajouter rate limiting webhook (10 req/min)

---

## 🔗 Ressources officielles

- [Documentation Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Cartes de test Stripe](https://stripe.com/docs/testing)
- [Webhooks Stripe](https://stripe.com/docs/webhooks)
- [SDK Python Stripe](https://stripe.com/docs/api/python)

---

**Dernière mise à jour :** 8 novembre 2025
**Auteur :** Matthieu (Pyx Digital Marketplace)
**Version intégration :** v0.3.0
