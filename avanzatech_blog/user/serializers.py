from rest_framework import serializers

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
