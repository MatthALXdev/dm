# Plan de charge – Projet DM (Digital Wallpapers)

> **Période couverte** : Sprint 1 (S1) et Sprint 2 (S2)
> **Date de génération** : 2025-10-07
> **Objectif** : Livrer v2.0.0 (MVP e-commerce complet)

---

## 📊 État d'avancement actuel

### ✅ Réalisé (Sprint 1)

| Version | Étape | Statut | Temps passé | Date livraison |
|---------|-------|--------|-------------|----------------|
| v0.0.1  | S1E1  | ✅ Terminé | 4-6h | 2025-XX-XX |
| v0.0.2  | S1E2  | ✅ Terminé | 1.5h | 2025-XX-XX |
| v0.1.0  | S1E3  | ✅ Terminé | 4-8h | 2025-XX-XX |

**Commits actuels** :
- `3ef120f` : v0.1.0 – Product model + pages catalog/product
- `4d1f6f2` : feat: /home page + redirection racine
- `d8c2e66` : feat: init Django project (hello world)

**Branche** : `main`

---

## 🚧 Travaux restants – Sprint 1

### v0.2.0 – Stripe Checkout (mode test)
**Étape** : S1E4 (en cours)
**Estimation** : 3-6h
**Dépendances** : v0.1.0 terminée ✅

**Livrables** :
- [ ] Modèle `Order` (id, produit, email, statut, date)
- [ ] Page produit avec bouton paiement → Stripe Checkout
- [ ] Webhook Stripe basique (`checkout.session.completed`)
- [ ] Documentation (s1_e4.md)
- [ ] Tag Git `v0.2.0`

**Planning** :
- Début estimé : 2025-10-08
- Fin estimée : 2025-10-09

---

### v0.2.1 – Page `/thanks`
**Estimation** : 0.5-1h
**Dépendances** : v0.2.0 terminée

**Livrables** :
- [ ] Page de remerciement après paiement
- [ ] Tag Git `v0.2.1`

**Planning** :
- Date estimée : 2025-10-09

---

### v0.3.0 – Webhook Stripe + création Order
**Estimation** : 4-8h
**Dépendances** : v0.2.1 terminée

**Livrables** :
- [ ] Webhook Stripe complet
- [ ] Création automatique d'un `Order` en DB
- [ ] Tests unitaires webhook
- [ ] Tag Git `v0.3.0`

**Planning** :
- Début estimé : 2025-10-10
- Fin estimée : 2025-10-11

---

### v0.4.0 – Token de téléchargement (mock)
**Estimation** : 2-4h
**Dépendances** : v0.3.0 terminée

**Livrables** :
- [ ] Génération de token de téléchargement
- [ ] Page de téléchargement (mock)
- [ ] Tag Git `v0.4.0`

**Planning** :
- Date estimée : 2025-10-12

---

### v0.5.0 – Intégration Backblaze B2
**Estimation** : 4-8h
**Dépendances** : v0.4.0 terminée

**Livrables** :
- [ ] Configuration B2 (bucket, clés API)
- [ ] Génération d'URL presignées réelles
- [ ] Upload de fichiers de test
- [ ] Tag Git `v0.5.0`

**Planning** :
- Début estimé : 2025-10-13
- Fin estimée : 2025-10-14

---

### v0.6.0 – Email transactionnel (sandbox)
**Estimation** : 2-4h
**Dépendances** : v0.5.0 terminée

**Livrables** :
- [ ] Configuration Postmark/SES sandbox
- [ ] Template email avec lien téléchargement
- [ ] Envoi automatique post-paiement
- [ ] Tag Git `v0.6.0`

**Planning** :
- Date estimée : 2025-10-15

---

### v0.7.0 – UI MVP responsive
**Estimation** : 8-16h
**Dépendances** : v0.6.0 terminée

**Livrables** :
- [ ] Design responsive (mobile-first)
- [ ] Amélioration UX pages catalog/product
- [ ] Tests multi-devices
- [ ] Tag Git `v0.7.0`

**Planning** :
- Début estimé : 2025-10-16
- Fin estimée : 2025-10-18

---

### v0.8.0 – Sécurité prod minimale
**Estimation** : 3-6h
**Dépendances** : v0.7.0 terminée

**Livrables** :
- [ ] HSTS activé
- [ ] CSP défini
- [ ] Headers sécurisés (X-Frame-Options, etc.)
- [ ] Revue checklist sécurité S1
- [ ] Tag Git `v0.8.0`

**Planning** :
- Date estimée : 2025-10-19

---

### v0.9.0 – Déploiement VPS Hetzner
**Estimation** : 8-16h
**Dépendances** : v0.8.0 terminée

**Livrables** :
- [ ] Configuration VPS (Nginx + systemd)
- [ ] HTTPS via Cloudflare (Full Strict)
- [ ] Déploiement application
- [ ] Tests en production
- [ ] Tag Git `v0.9.0`

**Planning** :
- Début estimé : 2025-10-20
- Fin estimée : 2025-10-22

---

### v1.0.0 – Walking Skeleton complet (fin Sprint 1)
**Estimation** : 8-16h
**Dépendances** : v0.9.0 terminée

**Livrables** :
- [ ] Tests unitaires + E2E
- [ ] Monitoring `/health` activé
- [ ] Documentation complète Sprint 1
- [ ] Revue finale sécurité S1
- [ ] Tag Git `v1.0.0` 🎯

**Planning** :
- Début estimé : 2025-10-23
- Fin estimée : 2025-10-25

**📅 Fin estimée Sprint 1** : **2025-10-25**

---

## 🚀 Travaux – Sprint 2

### v1.1.0 – Back-office produits
**Estimation** : 4-8h
**Dépendances** : v1.0.0 terminée

**Livrables** :
- [ ] Admin Django amélioré
- [ ] CRUD complet sur produits
- [ ] Upload images produits
- [ ] Tag Git `v1.1.0`

**Planning** :
- Début estimé : 2025-10-26
- Fin estimée : 2025-10-27

---

### v1.2.0 – Panier d'achat (multi-produits)
**Estimation** : 8-12h
**Dépendances** : v1.1.0 terminée

**Livrables** :
- [ ] Modèle Cart + CartItem
- [ ] Ajout/suppression articles
- [ ] Total dynamique (JS + backend)
- [ ] Page panier
- [ ] Tag Git `v1.2.0`

**Planning** :
- Début estimé : 2025-10-28
- Fin estimée : 2025-10-30

---

### v1.3.0 – Checkout Stripe (mode réel/test switch)
**Estimation** : 6-10h
**Dépendances** : v1.2.0 terminée

**Livrables** :
- [ ] Configuration clés Stripe live/test
- [ ] Paiement commande complète
- [ ] Gestion erreurs paiement
- [ ] Tag Git `v1.3.0`

**Planning** :
- Début estimé : 2025-10-31
- Fin estimée : 2025-11-02

---

### v1.3.1 – Page confirmation commande
**Estimation** : 1-2h
**Dépendances** : v1.3.0 terminée

**Livrables** :
- [ ] Page récapitulatif commande
- [ ] Affichage détails paiement
- [ ] Tag Git `v1.3.1`

**Planning** :
- Date estimée : 2025-11-03

---

### v1.4.0 – Téléchargement réel (B2 URLs presignées)
**Estimation** : 6-12h
**Dépendances** : v1.3.1 terminée

**Livrables** :
- [ ] URLs presignées sécurisées
- [ ] Expiration automatique (10 min)
- [ ] Contrôle d'accès (ordre payé requis)
- [ ] Tests téléchargement
- [ ] Tag Git `v1.4.0`

**Planning** :
- Début estimé : 2025-11-04
- Fin estimée : 2025-11-06

---

### v1.5.0 – Email client (prod)
**Estimation** : 2-4h
**Dépendances** : v1.4.0 terminée

**Livrables** :
- [ ] Configuration Postmark/SES prod
- [ ] Email avec lien téléchargement réel
- [ ] Tests envoi prod
- [ ] Tag Git `v1.5.0`

**Planning** :
- Date estimée : 2025-11-07

---

### v1.6.0 – UI améliorée (catalogue + checkout)
**Estimation** : 10-16h
**Dépendances** : v1.5.0 terminée

**Livrables** :
- [ ] Refonte design catalogue
- [ ] UX checkout fluide
- [ ] Responsive design revu
- [ ] Amélioration accessibilité
- [ ] Tag Git `v1.6.0`

**Planning** :
- Début estimé : 2025-11-08
- Fin estimée : 2025-11-11

---

### v1.7.0 – Authentification client
**Estimation** : 6-12h
**Dépendances** : v1.6.0 terminée

**Livrables** :
- [ ] Modèle User personnalisé
- [ ] Inscription + login
- [ ] Hash Argon2
- [ ] Validation email
- [ ] Espace client (commandes)
- [ ] Tag Git `v1.7.0`

**Planning** :
- Début estimé : 2025-11-12
- Fin estimée : 2025-11-14

---

### v1.8.0 – Sécurité & monitoring renforcés
**Estimation** : 6-10h
**Dépendances** : v1.7.0 terminée

**Livrables** :
- [ ] Rate limiting (login, webhook, download)
- [ ] Logs structurés
- [ ] Alertes paiement/webhook
- [ ] Revue checklist sécurité S2
- [ ] Tag Git `v1.8.0`

**Planning** :
- Début estimé : 2025-11-15
- Fin estimée : 2025-11-17

---

### v2.0.0 – MVP e-commerce complet (fin Sprint 2)
**Estimation** : 8-12h
**Dépendances** : v1.8.0 terminée

**Livrables** :
- [ ] Tests E2E complets
- [ ] Parcours client validé (bout en bout)
- [ ] Monitoring opérationnel
- [ ] Documentation complète Sprint 2
- [ ] Revue finale sécurité S2
- [ ] Tag Git `v2.0.0` 🎯

**Planning** :
- Début estimé : 2025-11-18
- Fin estimée : 2025-11-20

**📅 Fin estimée Sprint 2** : **2025-11-20**

---

## 📈 Synthèse de charge

### Sprint 1 (v0.1.0 → v1.0.0)

| Phase | Versions | Temps estimé | Temps réalisé |
|-------|----------|--------------|---------------|
| ✅ Réalisé | v0.0.1 - v0.1.0 | 5.5-11h | ~9.5-15.5h |
| 🚧 Restant | v0.2.0 - v1.0.0 | 40.5-69h | - |
| **Total S1** | **v0.0.1 - v1.0.0** | **46-80h** | **~9.5-15.5h** |

**Progression Sprint 1** : ~16-20% (3 versions sur 11)

### Sprint 2 (v1.1.0 → v2.0.0)

| Phase | Versions | Temps estimé |
|-------|----------|--------------|
| À faire | v1.1.0 - v2.0.0 | 57-88h |
| **Total S2** | **v1.1.0 - v2.0.0** | **57-88h** |

**Progression Sprint 2** : 0% (non démarré)

### Total projet (jusqu'à fin S2)

| Indicateur | Valeur basse | Valeur haute |
|------------|--------------|--------------|
| Temps estimé total | **103h** (~13 jours) | **168h** (~21 jours) |
| Temps déjà investi | 9.5h | 15.5h |
| Temps restant | 93.5h (~12 jours) | 152.5h (~19 jours) |
| **Progression globale** | **9%** | **9%** |

---

## 🎯 Jalons clés (milestones)

| Jalon | Version | Date cible | Statut |
|-------|---------|------------|--------|
| Walking Skeleton | v1.0.0 | 2025-10-25 | 🚧 En cours |
| MVP e-commerce | v2.0.0 | 2025-11-20 | ⏳ À venir |

---

## ⚠️ Risques & dépendances

### Risques identifiés

1. **Intégration Stripe** (v0.2.0 - v1.3.0)
   - Complexité webhook + gestion erreurs
   - Mitigation : tests approfondis en mode test avant live

2. **Backblaze B2** (v0.5.0, v1.4.0)
   - Première intégration, courbe d'apprentissage
   - Mitigation : documentation B2 + exemples SDK

3. **Déploiement VPS** (v0.9.0)
   - Configuration serveur, possibles blocages infrastructure
   - Mitigation : checklist détaillée + tests préalables

4. **Authentification** (v1.7.0)
   - Sécurité critique, risque d'erreur
   - Mitigation : utilisation Django User + Argon2 (standards éprouvés)

### Dépendances externes

- Comptes Stripe (test + live)
- Compte Backblaze B2
- Compte Postmark/AWS SES
- VPS Hetzner
- Domaine + Cloudflare

---

## 📝 Notes méthodologiques

### Approche de développement
- **Incrémentale** : chaque version apporte une fonctionnalité complète
- **Sécurisée** : revue checklist à chaque sprint
- **Versionnée** : tag Git systématique

### Estimation de temps
- **Fourchette basse** : développeur expérimenté Django/Stripe
- **Fourchette haute** : inclut apprentissage + debugging + documentation

### Livrables par version
- Code fonctionnel + tests
- Migration DB appliquée
- Documentation mise à jour
- Tag Git + commit descriptif

---

## 🔄 Historique des modifications

| Date | Modification | Auteur |
|------|--------------|--------|
| 2025-10-07 | Création initiale du plan de charge S1+S2 | Claude |

---

**Fin du plan de charge – Projet DM**
