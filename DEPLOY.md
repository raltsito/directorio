# Despliegue en Railway

El proyecto Django vive en el subdirectorio `Directorio/`. La configuracion de
Railway esta en la raiz del repo, asi que el **Root Directory** del servicio
debe quedar en `/` (el valor por defecto).

## 1. Variables de entorno del servicio

En Railway: servicio > pestana **Variables**.

| Variable | Valor | Obligatoria |
|---|---|---|
| `SECRET_KEY` | una clave larga y aleatoria (ver abajo) | Si |
| `DEBUG` | `False` | Si |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Para entrar al panel |
| `DJANGO_SUPERUSER_PASSWORD` | una contrasena fuerte | Para entrar al panel |
| `DJANGO_SUPERUSER_EMAIL` | tu correo | No |
| `ALLOWED_HOSTS` | dominios propios extra, separados por coma | Solo con dominio propio |
| `CSRF_TRUSTED_ORIGINS` | `https://tudominio.com` | Solo con dominio propio |
| `WEB_CONCURRENCY` | `2` | No |

El dominio `*.railway.app` ya viene permitido en `settings.py`, no hace falta
configurarlo.

Para generar la `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

## 2. Base de datos

En el proyecto de Railway: **New > Database > Add PostgreSQL**. Al enlazarla,
Railway inyecta `DATABASE_URL` y el proyecto la usa automaticamente.

Sin `DATABASE_URL` el proyecto cae a SQLite, que en Railway **se borra en cada
redeploy** (el sistema de archivos del contenedor es efimero). Para uso real,
Postgres es obligatorio.

Los 14 contactos actuales se cargan solos en el primer `migrate`
(`contactos/migrations/0002_contactos_iniciales.py`). La siembra solo ocurre si
la tabla esta vacia, asi que lo que edites despues en el admin no se pisa en
los siguientes deploys.

## 3. Que pasa en cada deploy

- **Build:** instala `requirements.txt` y corre `collectstatic` (los estaticos
  del admin los sirve WhiteNoise).
- **Start** (`start.sh`): `migrate` > `ensure_superuser` > `gunicorn` en `$PORT`.
- **Healthcheck:** `GET /healthz`, que verifica app + conexion a la base.

## 4. Rutas

| Ruta | Que es |
|---|---|
| `/` | el directorio de contactos |
| `/admin/` | panel para dar de alta, editar y dar de baja contactos |
| `/healthz` | healthcheck (JSON) |

## 5. Desarrollo local

```bash
python -m venv venv
venv/Scripts/activate        # en Windows
pip install -r requirements.txt
cd Directorio
python manage.py migrate
python manage.py runserver
```

En local, sin variables de entorno, usa SQLite y `DEBUG=False`. Si quieres los
mensajes de error detallados, exporta `DEBUG=True`.

El bloque que fuerza HTTPS (redirect a https, cookies `Secure`, HSTS) solo se
activa cuando detecta que corre en Railway, asi que `runserver` sobre
`http://127.0.0.1:8000` funciona normal.
