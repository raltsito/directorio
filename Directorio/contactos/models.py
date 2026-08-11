from django.db import models


class Contacto(models.Model):

    nombre = models.CharField(max_length=150)

    departamento = models.CharField(max_length=100)

    cargo = models.CharField(max_length=150)

    correo = models.EmailField()

    telefono = models.CharField(max_length=30)

    extension = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    ciudad = models.CharField(max_length=100)

    activo = models.BooleanField(default=True)

    fecha_ingreso = models.DateField(
        blank=True,
        null=True
    )

    fecha_baja = models.DateField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre