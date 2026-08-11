"""Carga los contactos iniciales para que la base de produccion no arranque vacia.

Solo siembra si la tabla esta vacia, asi los cambios hechos despues desde el
admin nunca se sobrescriben en un redeploy.
"""

import json
from pathlib import Path

from django.core.management.color import no_style
from django.db import migrations

FIXTURE = (
    Path(__file__).resolve().parent.parent / "fixtures" / "contactos_iniciales.json"
)


def cargar_contactos(apps, schema_editor):
    Contacto = apps.get_model("contactos", "Contacto")

    if Contacto.objects.exists():
        return

    with FIXTURE.open(encoding="utf-8") as archivo:
        registros = json.load(archivo)

    Contacto.objects.bulk_create(
        Contacto(pk=registro["pk"], **registro["fields"])
        for registro in registros
    )

    # bulk_create con pk explicito no avanza la secuencia en Postgres.
    # El estilo es obligatorio: el backend de Postgres lo usa para colorear el
    # SQL, y pasar None revienta con AttributeError.
    conexion = schema_editor.connection
    sentencias = conexion.ops.sequence_reset_sql(no_style(), [Contacto])

    if sentencias:
        with conexion.cursor() as cursor:
            for sentencia in sentencias:
                cursor.execute(sentencia)


def borrar_contactos(apps, schema_editor):
    Contacto = apps.get_model("contactos", "Contacto")

    with FIXTURE.open(encoding="utf-8") as archivo:
        registros = json.load(archivo)

    Contacto.objects.filter(
        pk__in=[registro["pk"] for registro in registros]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("contactos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_contactos, borrar_contactos),
    ]
