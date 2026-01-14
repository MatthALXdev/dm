"""
Gunicorn Configuration for Pyx (DM) - Production
=================================================

Configuration optimisée pour un serveur WSGI Django en production.
"""

import multiprocessing

# Nombre de workers (processus parallèles pour gérer les requêtes)
# Formule recommandée: (2 * CPU_COUNT) + 1
# Pour 3 workers fixes comme demandé:
workers = 3

# Type de worker (sync = standard pour Django sans async)
worker_class = 'sync'

# Connexions simultanées par worker (default: 1000)
worker_connections = 1000

# Adresse d'écoute (toutes les interfaces, port 8000)
bind = '0.0.0.0:8000'

# Timeout pour les requêtes (30 secondes)
# Si une requête prend plus de 30s, le worker est tué et redémarré
timeout = 30

# Keep-alive (secondes) pour les connexions HTTP persistantes
keepalive = 2

# Nombre maximum de requêtes qu'un worker peut traiter avant redémarrage
# Utile pour éviter les fuites mémoire
max_requests = 1000
max_requests_jitter = 50  # Ajoute une variation aléatoire (évite restart simultané)

# Logs
# '-' = stdout/stderr (capturé par Docker)
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Format des logs d'accès (Apache-like)
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Préchargement de l'application (économie mémoire, partage code entre workers)
preload_app = True

# Nombre de threads par worker (1 = sync pure)
threads = 1

# Processus daemon (False car Docker gère déjà ça)
daemon = False

# PID file (non nécessaire avec Docker)
pidfile = None

# User/Group (Docker gère les permissions)
user = None
group = None

# Temp directory
tmp_upload_dir = None
