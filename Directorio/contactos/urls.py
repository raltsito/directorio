from django.urls import path
from .views import directorio, healthz


urlpatterns = [
    path("", directorio, name="directorio"),
    path("healthz", healthz, name="healthz"),
]
