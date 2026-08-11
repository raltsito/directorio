from django.urls import path
from .views import directorio


urlpatterns = [
    path("", directorio, name="directorio"),
]