# DJANGO IMPORTS
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import generics, status
from rest_framework.response import Response

# MODELS
from .models import CustomUsers

# SERIALIZERS
from .serializers import UsersModelSerializer

# PERMISSIONS
from base.permissions import IsSuperuser


class UsersListAPIView(generics.ListAPIView):
    '''
    It shows all the users on the blogging platform. Only accessible for SUPERUSER
    '''
    queryset = CustomUsers.objects.all()
    serializer_class = UsersModelSerializer
    permission_classes = [IsSuperuser]


class UsersCreateAPIView(generics.CreateAPIView):
    '''
    It creates a new user on the blogging platform with configurable role and team fields. Only accessible for SUPERUSER
    '''
    serializer_class = UsersModelSerializer
    permission_classes = [IsSuperuser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = {'errors': []}

        is_active = serializer.validated_data.get('is_active')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')
        team = serializer.validated_data.get('team')
        first_name = serializer.validated_data.get('first_name')

        if not is_active:
            is_active = True

        if not email:
            error['errors'].append('Email address field may not be blank.')

        if not password:
            error['errors'].append('Password field may not be blank.')
        
        if not first_name:
            first_name = None
        
        if not role:
            role = 'blogger'

        if role == 'blogger' and not team:
            error['errors'].append('Bloggers must belong to one team.')

        if error['errors']:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        email = BaseUserManager.normalize_email(email)
        password = make_password(password)

        serializer.save(is_active=is_active, first_name=first_name, role=role)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersUpdateAPIView(generics.UpdateAPIView):
    '''
    It edits the specified user (path param) on the blogging platform. Only accessible for SUPERUSER
    '''
    queryset = CustomUsers.objects.all()
    serializer_class = UsersModelSerializer
    permission_classes = [IsSuperuser]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        error = {'errors': []}

        is_active = serializer.validated_data.get('is_active')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        instance_role = serializer.instance.role
        role = serializer.validated_data.get('role')
        team = serializer.validated_data.get('team')
        first_name = serializer.validated_data.get('first_name')

        if not is_active:
            is_active = True
        
        if email:
            email = BaseUserManager.normalize_email(email)
        else:
            email = serializer.instance.email
        
        if password:
            password = make_password(password)
        else:
            password = serializer.instance.password
        
        if instance_role == 'admin' and role == 'blogger' and not team:
            error['errors'].append('Bloggers must belong to one team.')
        elif instance_role == 'blogger' and role == 'admin' and not team:
            team = ''
        elif not role and not team:
            role = instance_role
            team = serializer.instance.team
        elif not team:
            team = serializer.instance.team
        
        if not first_name:
            first_name = serializer.instance.first_name
        
        if error['errors']:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(is_active=is_active, email=email, password=password, role=role, team=team, first_name=first_name)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UsersDeleteAPIView(generics.DestroyAPIView):
    '''
    It deletes (soft delete) the specified user (path param) on the blogging platform. Only accessible for SUPERUSER
    '''
    queryset = CustomUsers.objects.all()
    serializer_class = UsersModelSerializer
    permission_classes = [IsSuperuser]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
