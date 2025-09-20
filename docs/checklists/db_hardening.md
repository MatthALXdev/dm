# DB_HARDENING.md

## 1. Résumé / Contexte

- Base de données utilisée : **PostgreSQL** (prod), **SQLite** (dev).
- Objectif : réduire la surface d’attaque DB, sécuriser l’accès et garantir la résilience (sauvegardes/restauration).
- Niveau d’application : obligatoire en production, recommandé en staging, optionnel en dev.

---

## 2. Principes directeurs

- Principe de **moindre privilège** (least privilege).
- Séparation stricte des environnements (dev/staging/prod).
- Rotation régulière des credentials.
- Journalisation & monitoring activés.

---

## 3. Accounts & privilèges

- Créer un rôle applicatif limité (ex : `dm_app`) **sans superuser**.

```sql
CREATE ROLE dm_app LOGIN PASSWORD '<TO_FILL>' NOINHERIT;
GRANT CONNECT ON DATABASE dm_db TO dm_app;
GRANT USAGE ON SCHEMA public TO dm_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dm_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dm_app;
```

- Rôles séparés pour tâches admin/backups (ex : `dm_admin`).
- Ne pas utiliser `postgres` superuser pour l’app en prod.

---

## 4. Connexions & réseau

- Restreindre l’accès réseau au port PostgreSQL (5432) via firewall (UFW/iptables/Cloud provider rules).
- Autoriser uniquement l’app server, CI/CD et IP admin.
- Requérir TLS (SSL) pour connexions DB en prod.

---

## 5. Authentication & secrets

- Stocker les credentials uniquement via **variables d’environnement** ou secret manager (jamais dans Git).
- Exemples : `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.
- Documenter une procédure de rotation (qui, quand, comment invalider).

---

## 6. Chiffrement & données sensibles

- Mots de passe utilisateurs : hash Argon2 (via Django).
- Minimiser collecte de données personnelles (GDPR-lite).
- Pas de données PCI stockées (Stripe gère la carte).
- Optionnel : chiffrement au repos pour données sensibles supplémentaires.

---

## 7. Permissions DB & ORM

- Utiliser l’ORM Django (protège des injections SQL).
- Auditer les usages de `raw()` pour s’assurer qu’ils sont paramétrés.
- Vérifier périodiquement les privilèges via `\du` et `\dp`.

---

## 8. Backups & recovery

- Plan de sauvegarde : dump quotidien + point-in-time si possible.
- Stockage des backups chiffré (ex : B2 bucket privé).
- Procéder à des **tests de restauration** réguliers (≥ trimestriel).

---

## 9. Logging & monitoring

- Activer logs d’accès/erreurs Postgres.
- Centraliser logs (hors instance) pour analyse.
- Monitoring uptime `/health` + alerting webhook/email sur anomalies DB.
- Auditer accès administratifs.

---

## 10. Harden Postgres config

- Désactiver `trust` auth ; préférer `scram-sha-256`.
- Paramètres recommandés :

  ```
  log_min_error_statement = error
  log_connections = on
  log_disconnections = on
  ```

- Limiter `max_connections` selon charge attendue.

---

## 11. CI/CD & migrations

- Migrations exécutées par rôle admin restreint via CI/CD.
- Pas de dumps prod vers dev sans anonymisation.
- Secrets injectés par pipeline CI/CD ou systemd env.

---

## 12. Checklist Go-Live (Prod)

- [ ] App utilise un rôle applicatif limité ✅
- [ ] TLS activé entre app ↔ DB ✅
- [ ] Backups planifiés et testés ✅
- [ ] Rotation des credentials documentée ✅
- [ ] Monitoring DB opérationnel ✅

---

## 13. Procédure d’incident

- Révocation immédiate du rôle compromis.
- Rotation des credentials.
- Vérification des logs d’accès.
- Restauration depuis backup si corruption détectée.
- Communication interne + documentation incident.

---

## 14. Annexes

- Exemple `pg_hba.conf` minimal (prod) :

```
# TYPE  DATABASE  USER    ADDRESS         METHOD
host    dm_db     dm_app  10.0.0.0/24     scram-sha-256
```

- Exemple systemd service (env file avec PGPASSWORD).
- Références : [Postgres Security Best Practices](https://www.postgresql.org/docs/current/security.html).

---

**Responsable** : \[Nom/Admin]
**Dernière validation** : \[date]
