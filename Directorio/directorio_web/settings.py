"""
Django settings for directorio_web project.

Los valores sensibles y los que cambian entre local y produccion se leen de
variables de entorno. En local funciona sin configurar nada; en Railway se
toman las variables definidas en el servicio.
"""

import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(nombre, por_defecto=False):
    valor = os.environ.get(nombre)

    if valor is None:
        return por_defecto

    return valor.strip().lower() in ("1", "true", "yes", "on")


def env_list(nombre):
    valor = os.environ.get(nombre, "")

    return [item.strip() for item in valor.split(",") if item.strip()]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-p6yjrn3(ft^i6&^gqkmybi53=u+-&&wkt(mt%77isbb@q&+4qm",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool("DEBUG", por_defecto=False)

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS") or [
    "127.0.0.1",
    "localhost",
    "192.168.1.19",
]

CSRF_TRUSTED_ORIGINS = [
    origen if "://" in origen else f"https://{origen}"
    for origen in env_list("CSRF_TRUSTED_ORIGINS")
]

# Railway expone el dominio publico del servicio en esta variable.
RAILWAY_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

EN_RAILWAY = bool(RAILWAY_DOMAIN or os.environ.get("RAILWAY_ENVIRONMENT"))

if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_DOMAIN}")

# Cualquier subdominio de Railway (dominios de preview incluidos).
ALLOWED_HOSTS.append(".railway.app")
CSRF_TRUSTED_ORIGINS.append("https://*.railway.app")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'contactos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'directorio_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'directorio_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
#
# Si el servicio tiene una base Postgres enlazada usa DATABASE_URL; si no,
# cae a SQLite para desarrollo local.

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=False,
        ),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# El manifest (hash en el nombre del archivo) da cache infinito, pero exige que
# collectstatic se haya ejecutado. En Railway corre en el build; fuera de ahi
# usamos la variante sin manifest para no romper el desarrollo local.
STATICFILES_BACKEND = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if EN_RAILWAY
    else "whitenoise.storage.CompressedStaticFilesStorage"
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": STATICFILES_BACKEND,
    },
}

# Sirve los estaticos tambien cuando DEBUG=True, para que el admin se vea igual.
WHITENOISE_USE_FINDERS = DEBUG


# Seguridad detras del proxy de Railway

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

USE_X_FORWARDED_HOST = True

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# Lo que exige HTTPS solo se activa donde hay HTTPS: en local con runserver
# dejaria la app inaccesible (redirect a https) y sin poder iniciar sesion
# (cookies Secure sobre http).
HTTPS_ACTIVO = env_bool("HTTPS_ACTIVO", por_defecto=EN_RAILWAY and not DEBUG)

if HTTPS_ACTIVO:
    SECURE_SSL_REDIRECT = True
    # El healthcheck interno de Railway llega por HTTP plano: si lo redirigimos
    # a https el deploy se marca como fallido.
    SECURE_REDIRECT_EXEMPT = [r"^healthz$"]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# Email
# https://docs.djangoproject.com/en/6.0/topics/email/#topic-email-configuration

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
