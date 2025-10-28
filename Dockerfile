# Image de base : Python 3.11 (version stable, compatible Django 5)
FROM python:3.11-slim

# Variables d'environnement Python
# PYTHONUNBUFFERED=1 : Affiche les logs immédiatement (pas de buffer)
# PYTHONDONTWRITEBYTECODE=1 : Évite la création de fichiers .pyc (plus propre)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances système
# postgresql-client : Permet d'utiliser psql dans le conteneur (utile pour debug)
# build-essential : Nécessaire pour compiler psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
# On copie requirements.txt en premier pour profiter du cache Docker
# (si requirements.txt ne change pas, cette étape est réutilisée)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Copie du script d'entrypoint et rendre exécutable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposition du port 8000 (Django runserver par défaut)
EXPOSE 8000

# Commande par défaut (peut être overridée dans docker-compose.yml)
ENTRYPOINT ["/entrypoint.sh"]