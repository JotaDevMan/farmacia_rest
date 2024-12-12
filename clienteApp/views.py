from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests

# Create your views here.
@api_view(['GET', 'POST'])
def producto_lista(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def obtener_productos(request):
    try:
        # Asegúrate de usar la URL correcta de tu API
        api_url = "http://localhost:8000/api/"  # Ajusta esta URL según tu configuración
        response = requests.get(api_url)
        
        if response.status_code == 200:
            productos = response.json()
        else:
            productos = []
            print(f"Error en la solicitud: {response.status_code} - {response.reason}")
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        productos = []

    return render(request, 'index.html', {'productos': productos})