from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import JsonResponse
import json

from .models import Contacto


def healthz(request):
    """Healthcheck de Railway: confirma que la app responde y la BD contesta."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({"status": "ok"})
    except Exception as error:
        return JsonResponse({"status": "error", "detail": str(error)}, status=503)


def directorio(request):
    contactos = Contacto.objects.all().order_by("nombre")

    contactos_data = []

    for contacto in contactos:
        contactos_data.append({
            "id": contacto.id,
            "name": contacto.nombre,
            "dept": contacto.departamento,
            "role": contacto.cargo,
            "email": contacto.correo,
            "phone": contacto.telefono,
            "ext": contacto.extension or "",
            "city": contacto.ciudad,
        })

    contactos_json = json.dumps(
        contactos_data,
        cls=DjangoJSONEncoder
    )

    return render(
        request,
        "contactos/directorio.html",
        {
            "contactos_json": contactos_json,
        },
    )