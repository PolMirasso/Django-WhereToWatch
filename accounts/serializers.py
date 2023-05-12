from rest_framework import serializers
from django.contrib.auth.models import User
from .models import data_user
import os
from django.conf import settings
from django.core.exceptions import ValidationError

import string
import random

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    nsfw_content = serializers.IntegerField(source='data_user.nsfw_content')
    image_profile = serializers.ImageField(source='data_user.image_profile')
    description = serializers.CharField(source='data_user.description')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nsfw_content',
                  'image_profile', 'description')

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    nsfw_content = serializers.IntegerField(write_only=True)
    image_profile = serializers.ImageField(write_only=True)
    description = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'nsfw_content', 'image_profile', 'description')
        extra_kwargs = {'password': {'write_only': True}}


    
    def create(self, validated_data):
        email = validated_data.get('email')
        if email is None:
            raise serializers.ValidationError("El campo de correo electrónico es obligatorio.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email ya está registrado.")

        
        nsfw_content = validated_data.pop('nsfw_content')
        image_profile = validated_data.pop('image_profile')
        description = validated_data.pop('description')

        user = User.objects.create_user(**validated_data)

        # Rename the image file to the user's ID and random string
        ext = os.path.splitext(image_profile.name)[1]
        id_str = str(user.id)
        new_name = f"{id_str.join(random.choices(string.ascii_letters, k=8))}{ext}"
        image_profile.name = new_name

        # Save the image file to disk
        path = os.path.join(settings.MEDIA_ROOT, new_name)
        # with open(path, 'wb') as f:
        #     f.write(image_profile.read())

        data_user.objects.create(
            user=user, nsfw_content=nsfw_content, image_profile=image_profile, description=description)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("La nueva contraseña y la confirmación no coinciden.")
        return attrs

    def update(self, instance, validated_data):
        user = instance.user

        if not user.check_password(validated_data['old_password']):
            raise serializers.ValidationError("La contraseña anterior es incorrecta.")

        user.set_password(validated_data['new_password'])
        user.save()

        return user