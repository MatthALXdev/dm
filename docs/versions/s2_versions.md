# VERSIONS_SPRINT_2.md

## 🚀 Sprint 2 — Versions & Deliverables

**Prérequis :** Sprint 1 terminé (v1.0.0) avec paiement Stripe, tests et CI/CD fonctionnels

---

### v1.1.0 - Back-office produits amélioré
**Objectif :** Faciliter la gestion des produits via admin Django

**Features :**
- Personnalisation Django Admin pour modèle Product
- Colonnes display personnalisées (name, price, slug, created_at)
- Filtres latéraux (price range, date création)
- Actions bulk (activer/désactiver produits)
- Search fields (name, description)
- Ordering par défaut (date création desc)
- Preview image dans liste admin
- Inline editing amélioré

**Docs :**
- Guide utilisation admin Django
- Screenshots admin interface

⏱️ **Estimation : 4–8 h**

---

### v1.2.0 - Panier d'achat multi-produits
**Objectif :** Permettre achat de plusieurs produits en une commande

**Features :**
- Modèle `Cart` et `CartItem` (session-based ou DB)
- Vue ajout produit au panier
- Vue liste panier avec quantités
- Vue suppression article du panier
- Calcul total dynamique (subtotal + total)
- Bouton "Ajouter au panier" sur pages produit
- Page `/cart` avec récapitulatif
- Badge nombre articles dans header
- Persistence panier (cookie ou session)
- Bouton "Procéder au paiement" depuis panier

**UX :**
- Animations ajout panier
- Toast notifications
- Mise à jour quantités AJAX

**Docs :**
- Architecture panier (session vs DB)
- Guide gestion panier

⏱️ **Estimation : 8–12 h**

---

### v1.3.0 - Checkout Stripe multi-produits
**Objectif :** Adapter Stripe Checkout pour commandes complètes

**Features :**
- Modification `create_checkout_session` pour line_items multiples
- Calcul total panier
- Metadata enrichies (cart_id, items JSON)
- Modèle `Order` étendu (relation many-to-many avec Product via OrderItem)
- Modèle `OrderItem` (order, product, quantity, unit_price)
- Webhook adapté pour créer Order + OrderItems
- Page `/thanks` affiche liste produits commandés
- Vidage panier après paiement réussi

**Switch mode Stripe :**
- Configuration live/test keys via environnement
- Documentation passage en production

**Docs :**
- Guide checkout multi-produits
- Schéma base de données Order/OrderItem

⏱️ **Estimation : 6–10 h**

---

### v1.3.1 - Page confirmation de commande améliorée
**Objectif :** UX professionnelle post-paiement

**Features :**
- Design moderne page `/thanks`
- Récapitulatif détaillé commande (numéro, date, items, montant)
- Statut commande visuel
- Message personnalisé selon statut
- Bouton "Retour au catalogue"
- Section "Prochaines étapes" (email, téléchargement)

**UX :**
- Animations success
- Layout responsive
- Print-friendly CSS

⏱️ **Estimation : 1–2 h**

---

### v1.4.0 - Téléchargement réel via Backblaze B2
**Objectif :** Stocker et servir fichiers wallpapers sécurisés

**Features :**
- Compte Backblaze B2 configuré
- Bucket privé créé pour wallpapers
- SDK B2 Python installé
- Upload fichiers wallpapers vers B2
- Génération URLs presignées temporaires (expiration 24h)
- Endpoint `/download/<order_id>/<product_id>/` sécurisé
- Vérification Order belongs to user
- Logging téléchargements
- Limitation nombre téléchargements par commande

**Sécurité :**
- URLs expirables
- Validation ownership Order
- Rate limiting téléchargements

**Docs :**
- Guide configuration Backblaze B2
- Guide upload wallpapers
- Politique téléchargements

⏱️ **Estimation : 6–12 h**

---

### v1.5.0 - Email client avec lien téléchargement
**Objectif :** Automatiser envoi email post-achat

**Features :**
- Configuration service email (Postmark ou AWS SES)
- Template email HTML responsive
- Contenu email (confirmation commande, récapitulatif, lien téléchargement)
- Envoi email déclenché par webhook Stripe
- Gestion erreurs envoi email (retry, logging)
- Email inclut expiration lien téléchargement
- Test sandbox email validé

**Templates :**
- Email confirmation commande (HTML + plain text)
- Footer avec branding Pyx
- CTA clair vers téléchargement

**Docs :**
- Guide configuration Postmark/SES
- Exemples templates email

⏱️ **Estimation : 2–4 h**

---

### v1.6.0 - UI améliorée catalogue + checkout
**Objectif :** Raffiner design pour expérience premium

**Features :**
- Refonte grid catalog (masonry layout ou grid avancé)
- Filtres produits (prix, catégories)
- Tri produits (prix asc/desc, date, popularité)
- Prévisualisation image hover (zoom, lightbox)
- Animations scroll (fade-in, parallax)
- Design checkout multi-étapes (cart → infos → paiement)
- Progress bar checkout
- Optimisation performance images (lazy loading, WebP)
- Dark mode toggle (optionnel)

**Responsive :**
- Breakpoints optimisés (mobile S/M/L, tablet, desktop)
- Touch gestures mobile

**Docs :**
- Design system documentation
- Guide composants UI

⏱️ **Estimation : 10–16 h**

---

### v1.7.0 - Authentification client minimale
**Objectif :** Comptes utilisateurs pour historique commandes

**Features :**
- Modèle `CustomUser` étendu (email unique, first_name, last_name)
- Pages inscription/connexion/déconnexion
- Validation email (confirmation link)
- Hash mots de passe sécurisé (Argon2 ou PBKDF2)
- Page profil utilisateur
- Historique commandes utilisateur
- Association Order → User
- Protection routes (login_required)
- Reset mot de passe par email

**UX :**
- Formulaires validation frontend
- Messages d'erreur clairs
- Redirect après login vers page demandée

**Sécurité :**
- Rate limiting login
- CAPTCHA sur inscription (optionnel)
- Session timeout configurée

**Docs :**
- Guide authentification
- Politique confidentialité données

⏱️ **Estimation : 6–12 h**

---

### v1.8.0 - Sécurité & monitoring renforcés
**Objectif :** Préparer production réelle avec monitoring

**Features :**
- Rate limiting global (django-ratelimit)
- Headers sécurité (HSTS, CSP, X-Content-Type-Options)
- Logging structuré (rotation fichiers, niveaux)
- Monitoring Sentry pour erreurs
- Alertes paiement échoué
- Alertes webhook Stripe échec
- Dashboard monitoring basique (uptime, erreurs, commandes)
- Backup automatique DB (cron)
- Variables environnement validation (django-environ)

**Sécurité avancée :**
- SECRET_KEY rotation documentation
- ALLOWED_HOSTS strict
- SECURE_SSL_REDIRECT activé
- SESSION_COOKIE_SECURE activé

**Docs :**
- Guide sécurité production
- Guide monitoring et alertes
- Runbook incidents

⏱️ **Estimation : 6–10 h**

---

### v2.0.0 🎯 OBJECTIF SPRINT 2 - MVP E-commerce Complet
**Objectif :** Plateforme e-commerce production-ready end-to-end

**Récapitulatif features :**
- Parcours complet : catalogue → panier → paiement → email → téléchargement
- Authentification utilisateurs avec historique
- Back-office admin complet
- Paiement Stripe multi-produits
- Stockage Backblaze B2 sécurisé
- Email transactionnel automatique
- UI/UX premium responsive
- Sécurité production (HSTS, CSP, rate limiting)
- Monitoring et alertes opérationnels
- Tests E2E complets
- Documentation exhaustive

**Tests finaux :**
- Parcours client complet end-to-end
- Tests paiement Stripe live mode
- Tests téléchargement fichiers réels
- Tests emails production
- Tests charge (performance)
- Tests sécurité (OWASP Top 10)

**Livrables finaux :**
- Application production-ready
- Documentation utilisateur et technique
- Runbook opérationnel
- Plan marketing/lancement (optionnel)

**Démo entretien Sprint 2 :**
> "Pyx est une plateforme e-commerce complète : paiement Stripe multi-produits, téléchargement sécurisé Backblaze B2, email automatique, authentification utilisateurs, monitoring Sentry, tests E2E. Production-ready sur pyx.devamalix.fr."

⏱️ **Estimation finale : 8–12 h** (validation E2E + docs finales)

---

## 📊 Récapitulatif Sprint 2

### Temps total Sprint 2

| Phase | Versions | Estimation | Priorité |
|-------|----------|------------|----------|
| **Admin + Panier** | v1.1.0 → v1.2.0 | 12-20h | 🔴 Haute |
| **Checkout multi** | v1.3.0 → v1.3.1 | 7-12h | 🔴 Haute |
| **Download + Email** | v1.4.0 → v1.5.0 | 8-16h | 🟡 Moyenne |
| **UI Premium** | v1.6.0 | 10-16h | 🟢 Basse |
| **Auth + Sécurité** | v1.7.0 → v1.8.0 | 12-22h | 🟡 Moyenne |
| **Finalisation** | v2.0.0 | 8-12h | 🔴 Haute |

**Total Sprint 2 :** 57-98h (8-14 jours de travail)

---

## 🎯 Approche recommandée Sprint 2

### Phase 1 - Fonctionnel (priorité haute)
1. v1.1.0 - Admin (4-8h)
2. v1.2.0 - Panier (8-12h)
3. v1.3.0 - Checkout multi (6-10h)

**Livrable intermédiaire :** Panier + paiement multi-produits fonctionnel

### Phase 2 - Expérience utilisateur (priorité moyenne)
4. v1.4.0 - Download B2 (6-12h)
5. v1.5.0 - Email (2-4h)
6. v1.7.0 - Auth (6-12h)

**Livrable intermédiaire :** Parcours complet automatisé

### Phase 3 - Polish + Production (priorité selon besoin)
7. v1.6.0 - UI Premium (10-16h) - **Optionnel si deadline**
8. v1.8.0 - Sécurité (6-10h)
9. v2.0.0 - Validation (8-12h)

**Livrable final :** Production-ready

---

## 📝 Notes importantes

### Quand démarrer Sprint 2 ?
**Après Sprint 1 v1.0.0 accompli :**
- Stripe Checkout fonctionnel
- Tests + CI/CD en place

Sprint 2 = évolution professionnelle **pendant** l'alternance.

### Priorisation Sprint 2
Si temps limité :
- 🔴 **Critique :** v1.1.0, v1.2.0, v1.3.0 (panier + checkout)
- 🟡 **Important :** v1.4.0, v1.5.0, v1.7.0, v1.8.0 (download + email + auth)
- 🟢 **Nice to have :** v1.6.0 (UI premium)

---

**Dernière mise à jour :** 08 novembre 2025  
