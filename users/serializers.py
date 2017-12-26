from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()  # read only
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crea una instancia de un objeto User a partir de los datos de
        validated_data que contiene valores deserializados.
        """
        instance = User()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        """
        Crea una instancia de un objeto User a partir de los datos de
        validated_data que contiene valores deserializados.
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate_username(self, data):
        """
        Valida si existe un usuario con ese username
        """
        user = User.objects.filter(username=data)
        # Si estoy creando (no hay instancia) comprobar si hay usuarios con ese
        # username
        if not self.instance and len(user) != 0:
            raise ValidationError(u"Ya existe un usuario con ese username")
        # Si estoy actualizando (hay instancia) y estamos cambiando el username
        # y existen usuarios con el nuevo username
        elif self.instance and self.instance.username != data and len(user) != 0:
            raise ValidationError(u"Ya existe un usuario con ese username")
        else:
            return data
