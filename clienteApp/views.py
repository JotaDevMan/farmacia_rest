from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
import requests
from django.shortcuts import redirect

# Create your views here.
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def producto_lista(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)

        # Verificar el formato de la solicitud
        if request.accepted_renderer.format == 'html':
            # Renderizar template HTML
            return Response({'productos': serializer.data}, template_name='api_template.html')

        # Respuesta en JSON
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Renderizar template HTML después de guardar un producto
            if request.accepted_renderer.format == 'html':
                productos = Producto.objects.all()
                serializer = ProductoSerializer(productos, many=True)
                return Response({'productos': serializer.data}, template_name='api_template.html')

            # Respuesta en JSON
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Manejar errores de validación
        if request.accepted_renderer.format == 'html':
            return Response({'errors': serializer.errors}, template_name='api_template.html', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def producto_detalles(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        if request.accepted_renderer.format == 'html':
            return Response({'error': 'Producto no encontrado'}, template_name='product_details.html', status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        if request.accepted_renderer.format == 'html':
            return Response({'producto': serializer.data}, template_name='product_details.html')
        return Response(serializer.data)

    # Procesar PUT y DELETE simulados desde el formulario
    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        # Editar producto (PUT)
        if method == 'PUT':
            serializer = ProductoSerializer(producto, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                if request.accepted_renderer.format == 'html':
                    return Response({'producto': serializer.data, 'success': 'Producto actualizado'}, template_name='product_details.html')
                return Response(serializer.data)
            if request.accepted_renderer.format == 'html':
                return Response({'producto': producto, 'errors': serializer.errors}, template_name='product_details.html', status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Eliminar producto (DELETE)
        elif method == 'DELETE':
            producto.delete()
            if request.accepted_renderer.format == 'html':
                return redirect('producto_lista')  # Redirige a la lista
            return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def obtener_productos(request):
    try:
        api_url = "http://localhost:8000/api/"
        headers = {'Accept': 'application/json'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            productos = response.json()
        else:
            productos = []
            print(f"Error en la solicitud: {response.status_code} - {response.reason}")
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        productos = []

    return render(request, 'index.html', {'productos': productos})