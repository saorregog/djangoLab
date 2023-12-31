# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import serializers

# MODELS
from .models import Posts


class PostsListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = (
            'id',
            'author',
            'title',
            'content',
            'read_permission',
            'edit_permission'
        )


class PostsCreateUpdateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = (
            'title',
            'content',
            'read_permission',
            'edit_permission'
        )


class PostsRetrieveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = (
            'author',
            'title',
            'content',
        )


class PostsDeleteModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ()
