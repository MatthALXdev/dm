#!/bin/bash
# =============================================================================
# Pyx PostgreSQL Backup Script
# =============================================================================
# Description: Automated backup for pyx_postgres container on VPS production
# Location: /home/ubuntu/infra/scripts/backup-pyx-db.sh
# Cron: 0 3 * * * /home/ubuntu/infra/scripts/backup-pyx-db.sh >> /home/ubuntu/backups/pyx/backup.log 2>&1
# =============================================================================

set -euo pipefail

# Configuration
CONTAINER="pyx_postgres"
DB_NAME="pyx_db"
DB_USER="pyx_user"
BACKUP_DIR="/home/ubuntu/backups/pyx"
RETENTION_DAYS=7

# Timestamp format
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_FILE="pyx-db-${TIMESTAMP}.sql.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

# =============================================================================
# Main
# =============================================================================

log "========== Starting Pyx database backup =========="

# Create backup directory if not exists
if [[ ! -d "$BACKUP_DIR" ]]; then
    mkdir -p "$BACKUP_DIR" || error_exit "Failed to create backup directory: $BACKUP_DIR"
    log "Created backup directory: $BACKUP_DIR"
fi

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    error_exit "Container ${CONTAINER} is not running"
fi

log "Container ${CONTAINER} is running"

# Perform backup with pg_dump
log "Starting pg_dump for database: $DB_NAME"

if docker exec "$CONTAINER" pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_PATH"; then
    # Verify backup file exists and has content
    if [[ -f "$BACKUP_PATH" && -s "$BACKUP_PATH" ]]; then
        BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
        log "Backup created successfully: $BACKUP_FILE ($BACKUP_SIZE)"
    else
        error_exit "Backup file is empty or not created"
    fi
else
    # Clean up failed backup
    rm -f "$BACKUP_PATH" 2>/dev/null
    error_exit "pg_dump failed"
fi

# Rotation: delete backups older than RETENTION_DAYS
log "Cleaning up backups older than ${RETENTION_DAYS} days..."
DELETED_COUNT=$(find "$BACKUP_DIR" -name "pyx-db-*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete -print | wc -l)

if [[ "$DELETED_COUNT" -gt 0 ]]; then
    log "Deleted $DELETED_COUNT old backup(s)"
else
    log "No old backups to delete"
fi

# Show current backups count
CURRENT_COUNT=$(find "$BACKUP_DIR" -name "pyx-db-*.sql.gz" -type f | wc -l)
log "Current backups in rotation: $CURRENT_COUNT"

log "========== Backup completed successfully =========="

exit 0
