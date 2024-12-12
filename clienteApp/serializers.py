from rest_framework import serializers
from .models import Producto, Trabajador
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TrabajadorRegistroSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    rut = serializers.CharField()

    class Meta:
        model = Trabajador
        fields = ['email', 'password', 'rut']  # Incluye solo los campos relevantes

    def validate_rut(self, value):
        if Trabajador.objects.filter(rut=value).exists():
            raise serializers.ValidationError("El RUT ya está registrado.")
        return value

    def create(self, validated_data):
        # Crear usuario
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Crear trabajador asociado
        trabajador = Trabajador.objects.create(
            user=user,
            rut=validated_data['rut']
        )
        return trabajador

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Verificar si los campos email y password están presentes
        if not email or not password:
            raise serializers.ValidationError("Email y contraseña son obligatorios.")

        # Intentar autenticar al usuario con el email
        user = authenticate(username=email, password=password)
        
        # Si no se encuentra el usuario, lanzar un error
        if user is None:
            raise serializers.ValidationError("Credenciales inválidas.")

        data['user'] = user  # Guardar el usuario autenticado en los datos validados
        return data