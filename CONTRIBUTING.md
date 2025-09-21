# 📝 Guide Git — Projet DM

## Flux de travail avant v1.0.0

- Tout le développement se fait directement sur la branche **`main`**.
- Chaque version correspond à :

  1. **Un commit clair** (ex. `feat: add /home page`).
  2. **Un tag Git** (ex. `v0.0.2`).

- On pousse toujours le commit + tag vers GitHub :

  ```bash
  git add .
  git commit -m "feat: add /home page"
  git tag v0.0.2
  git push origin main --tags
  ```

👉 Résultat : `main` contient uniquement des versions stables et identifiées.

---

## Flux de travail après v1.0.0

- La version **v1.0.0** est considérée comme le **socle stable**.
- Les évolutions se font via **branches temporaires** :

  - `bugfix/...` pour corriger un problème.
  - `feature/...` pour une nouvelle amélioration.

- Exemple :

  ```bash
  git checkout -b bugfix/fix-stripe-webhook
  # dev + commit
  git push origin bugfix/fix-stripe-webhook
  # testé → merge vers main
  git checkout main
  git merge bugfix/fix-stripe-webhook
  git tag v1.0.1
  git push origin main --tags
  ```

👉 Objectif : garder `main` toujours déployable et stable.

---

## Bonnes pratiques

- Un **commit = une version** (pas de commits intermédiaires brouillons).
- Toujours mettre un **message de commit clair** qui reflète le livrable.
- Ne pas oublier le **tag** : il est la référence principale pour la roadmap.
- Documenter les changements dans `progress/` et mettre à jour `VERSIONS.md` avant de taguer.
