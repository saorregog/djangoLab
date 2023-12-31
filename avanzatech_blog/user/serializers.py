# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import serializers

# MODELS
from .models import CustomUsers


class UsersModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsers
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'role',
            'team',
            'is_active'
        )
        extra_kwargs = {'password': {'write_only': True}}
