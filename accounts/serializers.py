from rest_framework import serializers
from django.contrib.auth.models import User
from .models import data_user
import os
from django.conf import settings
import os
from django.conf import settings

import string
import random

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source='data_user.age')
    image_profile = serializers.ImageField(source='data_user.image_profile')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'image_profile')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    image_profile = serializers.ImageField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'age', 'image_profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        age = validated_data.pop('age')
        image_profile = validated_data.pop('image_profile')
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

        data_user.objects.create(user=user, age=age, image_profile=image_profile)
        return user