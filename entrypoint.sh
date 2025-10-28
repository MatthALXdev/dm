#!/bin/bash
set -e

echo "🔄 Waiting for database..."
python << END
import sys
import time
import psycopg
from psycopg import OperationalError
import os

max_retries = 30
retry = 0

while retry < max_retries:
    try:
        conn = psycopg.connect(
            dbname=os.getenv('DB_NAME', 'dm_db'),
            user=os.getenv('DB_USER', 'dm_user'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'db'),
            port=os.getenv('DB_PORT', '5432')
        )
        conn.close()
        print("✓ Database is ready!")
        sys.exit(0)
    except OperationalError:
        retry += 1
        print(f"Database unavailable, waiting... ({retry}/{max_retries})")
        time.sleep(1)

print("✗ Could not connect to database")
sys.exit(1)
END

echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Load seed data only in development/test environments
# Production uses data migrations instead (see core/migrations/0003_load_initial_products.py)
if [ "${DJANGO_DEBUG}" = "1" ] || [ "${ENVIRONMENT}" = "development" ]; then
    echo "🌱 Loading seed data (dev/test mode)..."
    python seed.py
else
    echo "ℹ️  Skipping seed (production mode - using data migrations)"
fi

echo "✓ Initialization complete!"
echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
