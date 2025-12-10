#!/usr/bin/env bash
set -e

# Load .env if present (local dev convenience)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Wait for Postgres using a small Python check (portable)
echo "Waiting for Postgres..."
python - <<PY
import os,sys,time
import psycopg2
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    host = os.environ.get("POSTGRES_HOST","postgres")
    port = int(os.environ.get("POSTGRES_PORT",5432))
    user = os.environ.get("POSTGRES_USER","postgres")
    password = os.environ.get("POSTGRES_PASSWORD","postgres")
    db = os.environ.get("POSTGRES_DB","flashcart")
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
retries=0
while True:
    try:
        conn=psycopg2.connect(DATABASE_URL, connect_timeout=3)
        conn.close()
        print("Postgres reachable")
        break
    except Exception as e:
        retries+=1
        if retries>60:
            print("Postgres not reachable - exiting")
            sys.exit(1)
        time.sleep(1)
PY

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput

# If CMD provided, execute it; else start gunicorn by default
if [ $# -eq 0 ]; then
  exec gunicorn flashcart.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 2
else
  exec "$@"
fi
