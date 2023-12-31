# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import serializers

# MODELS
from .models import Likes


class LikeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = ()


class ListLikesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = (
            'id',
            'user',
            'post',
        )
