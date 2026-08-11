#!/usr/bin/env bash
# Arranque del servicio en Railway.
# El proyecto Django vive en el subdirectorio Directorio/.
set -euo pipefail

cd "$(dirname "$0")/Directorio"

echo "==> Aplicando migraciones"
python manage.py migrate --noinput

echo "==> Verificando superusuario"
python manage.py ensure_superuser

echo "==> Iniciando gunicorn en el puerto ${PORT:-8000}"
exec gunicorn directorio_web.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
