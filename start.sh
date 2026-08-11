#!/usr/bin/env bash
# Arranque del servicio en Railway.
# El proyecto Django vive en el subdirectorio Directorio/.
set -euo pipefail

cd "$(dirname "$0")/Directorio"

# La red privada de Railway (IPv6) tarda unos segundos en resolver al arrancar
# el contenedor: sin esta espera el primer migrate puede fallar por DNS.
if [ -n "${DATABASE_URL:-}" ]; then
    echo "==> Esperando a la base de datos"

    esperar_db='
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "directorio_web.settings")
django.setup()
from django.db import connection
connection.ensure_connection()
'

    for intento in $(seq 1 30); do
        if python -c "${esperar_db}" >/dev/null 2>&1; then
            echo "    base de datos lista (intento ${intento})"
            break
        fi

        if [ "${intento}" -eq 30 ]; then
            echo "    la base no respondio tras 30 intentos; error real:"
            python -c "${esperar_db}"
            exit 1
        fi

        sleep 2
    done
fi

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
