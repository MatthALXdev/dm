# Screenshots Guide

Ce dossier contient les screenshots de l'interface Pyx pour le README.

## 📸 Screenshots à capturer

### 1. screenshot-catalog.png
**Page :** http://localhost:8000/catalog/
- **Résolution :** 1920x1080 ou 1440x900
- **Contenu :** Grid de produits (3 produits visibles)
- **Points clés :** Header avec logo Pyx, cards produits avec images, prix, boutons

### 2. screenshot-product.png
**Page :** http://localhost:8000/product/pack-minimal/ (ou autre slug)
- **Résolution :** 1920x1080 ou 1440x900
- **Contenu :** Page détail produit
- **Points clés :** Image grande, description, prix, bouton "Acheter maintenant"

### 3. screenshot-thanks.png
**Page :** http://localhost:8000/thanks/?session_id=... (après achat test)
- **Résolution :** 1920x1080 ou 1440x900
- **Contenu :** Confirmation paiement
- **Points clés :** Message succès, montant, email, bouton "Télécharger"

### 4. screenshot-download.png
**Page :** http://localhost:8000/download/<token>/ (depuis page thanks)
- **Résolution :** 1920x1080 ou 1440x900
- **Contenu :** Page téléchargement sécurisée
- **Points clés :** Infos commande, compteur téléchargements, lien fichier

---

## 🛠️ Outils recommandés

### macOS
- **Cmd + Shift + 4** → Sélection zone
- Ou **Cmd + Shift + 3** → Plein écran

### Linux
- **Flameshot** : `flameshot gui`
- **GNOME Screenshot** : `gnome-screenshot -a`
- **Spectacle (KDE)** : `spectacle`

### Windows
- **Win + Shift + S** → Outil capture
- **Snipping Tool**

---

## 📐 Spécifications

### Format
- **Type :** PNG (pas JPG pour éviter compression)
- **Résolution :** 1920x1080 ou 1440x900
- **Ratio :** 16:9 ou 16:10

### Optimisation
Après capture, compresser avec :
- [TinyPNG](https://tinypng.com/) (en ligne)
- `pngquant` (CLI) : `pngquant --quality=65-80 screenshot.png`
- `optipng` (CLI) : `optipng -o7 screenshot.png`

**Objectif :** Réduire 50-70% taille sans perte visible

---

## ✅ Checklist capture

- [ ] Navigateur en mode fenêtré (pas plein écran)
- [ ] Zoom navigateur à 100%
- [ ] Barre d'adresse visible (optionnel mais pro)
- [ ] Pas de popups/modales ouvertes (sauf si pertinent)
- [ ] Données de test cohérentes (ex: email@exemple.com)
- [ ] Images produits chargées correctement
- [ ] Format PNG enregistré
- [ ] Fichiers optimisés (<500KB chacun)

---

## 📝 Nommage

Respecter exactement ces noms :
```
screenshot-catalog.png
screenshot-product.png
screenshot-thanks.png
screenshot-download.png
```

Ces noms sont référencés dans le README.md.

---

## 🚀 Workflow

1. Lancer l'application : `docker compose -f docker-compose.dev.yml up -d`
2. Ouvrir navigateur : http://localhost:8000/catalog/
3. Capturer 4 screenshots selon liste ci-dessus
4. Optimiser avec TinyPNG ou CLI
5. Placer dans ce dossier `docs/images/`
6. Commit : `git add docs/images/*.png && git commit -m "docs: add screenshots"`
7. Vérifier rendu dans README sur GitHub

---

**Dernière mise à jour :** 2025-12-09
