from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response


def create_update_validations(serializer):
    email = BaseUserManager.normalize_email(serializer.validated_data.get('email'))
    password = make_password(serializer.validated_data.get('password'))
    role = serializer.validated_data.get('role')
    team = serializer.validated_data.get('team')
    first_name = serializer.validated_data.get('first_name')

    if role == 'blogger' and not team:
        return Response({'error': 'Bloggers must belong to one team'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not first_name:
        first_name = None

    return serializer, email, password, first_name
