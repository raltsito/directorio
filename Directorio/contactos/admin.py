from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "departamento",
        "cargo",
        "correo",
        "telefono",
        "extension",
        "ciudad",
        "activo",
    )

    list_filter = (
        "departamento",
        "ciudad",
        "activo",
    )

    search_fields = (
        "nombre",
        "correo",
        "telefono",
        "cargo",
    )