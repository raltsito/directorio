"""Crea el superusuario del admin a partir de variables de entorno.

Se ejecuta en cada arranque: si el usuario ya existe no hace nada, y si no hay
password configurado simplemente lo omite sin fallar el despliegue.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el superusuario definido en DJANGO_SUPERUSER_* si no existe."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD sin "
                "definir: no se crea superusuario."
            )
            return

        if User.objects.filter(**{User.USERNAME_FIELD: username}).exists():
            self.stdout.write(f"El superusuario '{username}' ya existe.")
            return

        User.objects.create_superuser(
            username=username,
            email=email or None,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado."))
