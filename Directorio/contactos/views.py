from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import Contacto


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