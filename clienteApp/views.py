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
    

@api_view(['GET', 'PUT', 'DELETE'])
def producto_detalles(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def obtener_productos(request):
    try:
       
        api_url = "http://localhost:8000/api/"  
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