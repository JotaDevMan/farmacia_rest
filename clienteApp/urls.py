from django.urls import path
from clienteApp import views

urlpatterns = [
    path("", views.obtener_productos, name="index"),
    path("api/", views.producto_lista),
]
