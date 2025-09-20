# db_audit.ps1

<#!
Mini-script d’audit Postgres pour projet DM.
- Vérifie les rôles existants et leurs privilèges
- Vérifie les droits sur les tables du schéma public
- Vérifie la méthode d’authentification (pg_hba.conf)
- Ne modifie rien (lecture seule)
#>

param(
    [Parameter(Mandatory = $false)][string] $DbName = "dm_db",
    [Parameter(Mandatory = $false)][string] $DbUser = "postgres",
    [Parameter(Mandatory = $false)][string] $DbHost = "127.0.0.1",
    [Parameter(Mandatory = $false)][string] $DbPort = "5432"
)

Write-Output "=== Audit Postgres pour $DbName ==="

# Vérifie rôles et privilèges
Write-Output "`n[ROLES & PRIVILEGES]"
psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -c "\\du"

# Vérifie droits sur les tables du schéma public
Write-Output "`n[PERMISSIONS TABLES]"
psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -c "\\dp"

# Vérifie méthodes d’authentification (nécessite accès au serveur)
$pgHbaPath = "/etc/postgresql/$(psql -V | ForEach-Object { ($_ -split " ")[2] })/main/pg_hba.conf"
if (Test-Path $pgHbaPath) {
    Write-Output "`n[PG_HBA.CONF - AUTH METHODS]"
    Get-Content $pgHbaPath | Where-Object { $_ -notmatch "^#" -and $_.Trim() -ne "" }
}
else {
    Write-Output "`n[PG_HBA.CONF - AUTH METHODS] (non trouvé, vérifier chemin manuellement)"
}

Write-Output "`n=== Fin de l’audit (lecture seule, aucun changement effectué) ==="
