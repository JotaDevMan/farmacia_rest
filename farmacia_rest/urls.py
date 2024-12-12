from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ruta del administrador
    path("admin/", admin.site.urls),

    # Incluye las rutas específicas de la app clienteApp
    path("", include('clienteApp.urls')),  # Aquí rediriges al archivo clienteApp/urls.py
]
