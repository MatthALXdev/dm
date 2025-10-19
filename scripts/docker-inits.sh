#!/bin/bash

# Couleurs pour les logs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐋 Initialisation de DM avec Docker${NC}"

# 1. Vérifier que .env.docker existe
if [ ! -f .env.docker ]; then
    echo -e "${YELLOW}⚠️  Fichier .env.docker introuvable${NC}"
    echo "Copie de .env vers .env.docker..."
    cp .env .env.docker
    echo -e "${YELLOW}⚠️  IMPORTANT : Modifie DB_HOST=db dans .env.docker${NC}"
    exit 1
fi

# 2. Build des images Docker
echo -e "${GREEN}📦 Build des images Docker...${NC}"
docker-compose build

# 3. Démarrage de PostgreSQL
echo -e "${GREEN}🗄️  Démarrage de PostgreSQL...${NC}"
docker-compose up -d db

# 4. Attente que PostgreSQL soit prêt
echo -e "${GREEN}⏳ Attente que PostgreSQL soit prêt...${NC}"
sleep 10

# 5. Application des migrations
echo -e "${GREEN}🔄 Application des migrations...${NC}"
docker-compose run --rm web python manage.py migrate

# 6. Création du superuser (optionnel, interactif)
read -p "Créer un superuser ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose run --rm web python manage.py createsuperuser
fi

# 7. Collecte des fichiers statiques (optionnel pour v0.1.0)
echo -e "${GREEN}📁 Collecte des fichiers statiques...${NC}"
docker-compose run --rm web python manage.py collectstatic --noinput

# 8. Démarrage complet
echo -e "${GREEN}🚀 Démarrage de l'application...${NC}"
docker-compose up

echo -e "${GREEN}✅ DM accessible sur http://localhost:8000${NC}"
echo -e "${GREEN}✅ Admin accessible sur http://localhost:8000/admin${NC}"