#!/bin/sh
set -e

echo "==== Waiting for Postgres on $SQL_HOST:$SQL_PORT ===="
: "${SQL_HOST:?SQL_HOST is not set}"
: "${SQL_PORT:?SQL_PORT is not set}"

while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.1
done
echo "==== Postgres is up! ===="

echo "==== Running migrations... ===="
python manage.py migrate --noinput
echo "==== Migrations complete ===="

echo "==== Creating superuser (if not exists) ===="
python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print("==== Superuser created successfully ====")
        print(f"   Username: {username}")
        print(f"   Email:    {email}")
    else:
        print("==== Superuser already exists ====")
        print(f"   Username: {username}")
else:
    import sys
    print("==== ⚠️  Superuser credentials not set in .env, skipping creation ====", file=sys.stderr)
EOF

echo "==== Starting server with Gunicorn ===="
exec gunicorn event_manager.wsgi:application --bind 0.0.0.0:8000
