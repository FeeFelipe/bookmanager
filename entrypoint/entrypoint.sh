#!/bin/bash
set -e

# Função para aguardar serviço subir
wait_for_service() {
  local host=$1
  local port=$2
  local name=$3

  echo "Waiting for $name on $host:$port..."
  while ! nc -z "$host" "$port"; do
    sleep 0.5
  done
  echo "$name is up on $host:$port"
}

# Valores padrão (caso .env não tenha)
POSTGRES_HOST="${POSTGRES_HOST:-postgres}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
RABBITMQ_HOST="${RABBITMQ_HOST:-rabbitmq}"
RABBITMQ_PORT="${RABBITMQ_PORT:-5672}"

wait_for_service "$POSTGRES_HOST" "$POSTGRES_PORT" "PostgreSQL"
wait_for_service "$RABBITMQ_HOST" "$RABBITMQ_PORT" "RabbitMQ"

if [ "$ROLE" = "web" ]; then
  echo "Running migrations..."
  python manage.py makemigrations author
  python manage.py makemigrations branch
  python manage.py makemigrations book_category
  python manage.py makemigrations book
  python manage.py makemigrations book_stock
  python manage.py makemigrations
  python manage.py migrate

  echo "Creating default superuser (if not exists)..."
  python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "admin"
password = "admin123"
email = "admin@example.com"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

  echo "Starting Django server..."
  exec python manage.py runserver 0.0.0.0:8000

elif [ "$ROLE" = "worker" ]; then
  echo "Starting Dramatiq worker..."
  sleep 5
  python manage.py rundramatiq --processes 1 --threads 1
else
  echo "Unknown ROLE: $ROLE"
  exit 1
fi
