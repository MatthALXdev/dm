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

echo "✓ Initialization complete!"
echo "🚀 Starting Gunicorn server (3 workers, production-ready)..."
exec gunicorn backend.wsgi:application --config gunicorn.conf.py
