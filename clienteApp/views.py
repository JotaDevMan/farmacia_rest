from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET', 'POST'])
def producto_lista(request):
    if request.method == 'GET':
        employees = Producto.objects.all()
        serializer = ProductoSerializer(employees, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)