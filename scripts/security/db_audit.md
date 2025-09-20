# DB Audit Script

## 🎯 Objectif

`db_audit.ps1` est un script **d’audit en lecture seule** pour PostgreSQL.  
Il permet de vérifier rapidement l’état de la sécurité de la base de données dans le cadre du projet **DM**.

---

## 🔍 Ce que fait le script

- Liste les **rôles et privilèges** existants (`\du`).
- Liste les **droits sur les tables** du schéma public (`\dp`).
- Vérifie les **méthodes d’authentification** définies dans `pg_hba.conf` (si accessible).
- **Ne modifie rien** → 100% lecture seule.

---

## ▶️ Utilisation

Depuis PowerShell :

```powershell
# Exemple avec utilisateur postgres et base dm_db
.\db_audit.ps1 -DbUser postgres -DbName dm_db
```
