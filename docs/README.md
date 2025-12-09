# Documentation Pyx (DM)

Documentation technique du projet **Pyx** (Digital Marketplace).

---

## Structure de la documentation

### Fichier principal
- **[`../CHANGELOG.md`](../CHANGELOG.md)** - Historique complet des versions et modifications (à la racine du projet)

### Guides techniques
- **[`STRIPE_SETUP.md`](STRIPE_SETUP.md)** - Configuration et intégration Stripe (checkout + webhooks)
- **[`DOCKER-COMPOSE-CONFIGS.md`](DOCKER-COMPOSE-CONFIGS.md)** - Architecture Docker et environnements (dev/nexus/prod)
- **[`INFRASTRUCTURE.md`](INFRASTRUCTURE.md)** - Infrastructure nginx-static et Traefik

### Checklists opérationnelles
- [`checklists/dev_environment.md`](checklists/dev_environment.md) - Setup environnement développement
- [`checklists/deploy-vps-v0.2.0.md`](checklists/deploy-vps-v0.2.0.md) - Déploiement VPS production
- [`checklists/s1_security_checklist.md`](checklists/s1_security_checklist.md) - Checklist sécurité Sprint 1
- [`checklists/s2_security_checklist.md`](checklists/s2_security_checklist.md) - Checklist sécurité Sprint 2
- [`checklists/db_hardening.md`](checklists/db_hardening.md) - Sécurisation base de données

### Roadmap
- [`roadmap/s3_roadmap.md`](roadmap/s3_roadmap.md) - Roadmap Sprint 3 (features avancées)

### Archives
- [`archive/`](archive/) - Ancienne structure documentation (versions/progress par épisodes)

---

## Refactorisation documentation (2025-12-09)

### Ancien système (archivé)
```
docs/
├── versions/s1_versions.md      # Versions Sprint 1
├── versions/s2_versions.md      # Versions Sprint 2
├── progress/s1_e1.md            # Étapes détaillées Sprint 1
├── progress/s1_e2.md
├── ...
└── plan_de_charge_s1_s2.md      # Planning global
```

**Problèmes :**
- Documentation fragmentée (19 fichiers)
- Redondance entre `versions/` et `progress/`
- Maintenance lourde (mise à jour multi-fichiers)
- Navigation complexe

### Nouveau système (actuel)
```
CHANGELOG.md                      # Fichier unique à la racine (suivi versions/tags)
docs/
├── README.md                     # Ce fichier (index documentation)
├── STRIPE_SETUP.md               # Guides techniques (conservés)
├── DOCKER-COMPOSE-CONFIGS.md
├── INFRASTRUCTURE.md
├── checklists/                   # Checklists opérationnelles
├── roadmap/                      # Roadmap futures versions
└── archive/                      # Ancienne doc (référence historique)
```

**Avantages :**
- Un seul fichier de suivi (`CHANGELOG.md`)
- Format standard ([Keep a Changelog](https://keepachangelog.com/))
- Correspondance 1:1 avec tags Git
- Guides techniques conservés (peu de duplication)
- Navigation simplifiée

---

## Comment utiliser cette documentation

### Consulter l'historique des versions
Lire [`../CHANGELOG.md`](../CHANGELOG.md) pour voir toutes les modifications par version/tag.

### Configurer Stripe
Suivre [`STRIPE_SETUP.md`](STRIPE_SETUP.md) pour l'intégration complète (checkout + webhooks + tests).

### Déployer en production
1. Lire [`DOCKER-COMPOSE-CONFIGS.md`](DOCKER-COMPOSE-CONFIGS.md) pour comprendre les environnements
2. Suivre [`checklists/deploy-vps-v0.2.0.md`](checklists/deploy-vps-v0.2.0.md) pour le déploiement VPS
3. Appliquer [`checklists/s1_security_checklist.md`](checklists/s1_security_checklist.md) pour la sécurité

### Contribuer
1. Faire les modifications dans une branche feature
2. Mettre à jour `CHANGELOG.md` section `[Unreleased]`
3. Créer Pull Request
4. Après merge : créer tag + déplacer changements dans section versionnée

---

## Tags et versions

### Convention de versionnement
Semantic Versioning : `vMAJOR.MINOR.PATCH`

- **MAJOR** : Changements incompatibles API (breaking changes)
- **MINOR** : Nouvelles fonctionnalités (rétro-compatibles)
- **PATCH** : Corrections de bugs (rétro-compatibles)

### Correspondance tags Git
Chaque version dans `CHANGELOG.md` correspond à un tag Git :
```bash
git tag -l
# v0.0.1, v0.0.2, v0.1.0, v0.1.1, v0.1.2, v0.2.0, v0.2.1, v0.3.0, v0.4.0...
```

---

## Contact et support

- **Repository :** [MatthALXdev/dm](https://github.com/MatthALXdev/dm)
- **Issues :** [GitHub Issues](https://github.com/MatthALXdev/dm/issues)
- **Auteur :** Matthieu (Pyx/Devamalix)

---

**Dernière mise à jour :** 2025-12-09
**Version actuelle :** v0.4.0
