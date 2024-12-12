from django.db import models
from django.contrib.auth.models import User
import uuid 

# Modelos existentes
class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField(unique=True, max_length=12)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio = models.IntegerField()

class Ticket(models.Model):
    id_ticket = models.AutoField(primary_key=True)
    id_cliente_temporal = models.CharField(unique=True, max_length=15, default=uuid.uuid4().hex[:15])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    precio_total = models.IntegerField()

class DetalleTicket(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()