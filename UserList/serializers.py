from rest_framework import serializers
from .models import UserLists

class UserListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLists
        fields = ['list_id', 'list_name', 'list_content']
