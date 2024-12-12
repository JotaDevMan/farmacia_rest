
from django.contrib import admin
from django.urls import path, include
from clienteApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('clienteApp.urls'), name="index"),
    path("api/", views.producto_lista, name="producto_lista"),
    path('api/<int:pk>/', views.producto_detalles, name='producto_detalles'),
]
