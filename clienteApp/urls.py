from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path("", views.obtener_productos, name="index"),

    # API para productos
    path("api/productos/", views.producto_lista, name="producto_lista"),
    path("api/productos/<int:pk>/", views.producto_detalles, name="producto_detalles"),

    # API para autenticación
    path("api/iniciar-sesion/", views.api_iniciar_sesion, name="api_iniciar_sesion"),
    path("api/registro/", views.api_registro_trabajador, name="api_registro_trabajador"),

    # Vistas HTML para registro e inicio de sesión
    path("registro/", views.registro_trabajador, name="register"),
    path("iniciar-sesion/", views.iniciar_sesion, name="login"),
]
