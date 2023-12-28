from rest_framework import serializers

from .models import Comments


class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = (
            'content',
        )


class ListCommentsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = (
            'id',
            'user',
            'post',
            'content',
        )
