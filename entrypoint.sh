#!/bin/sh

echo "Czekam na bazę danych..."
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Postgres is up"

echo "Baza danych dostępna, uruchamiam migracje..."
python manage.py migrate --noinput

echo "Zbieram pliki statyczne..."
python manage.py collectstatic --noinput

exec "$@"
