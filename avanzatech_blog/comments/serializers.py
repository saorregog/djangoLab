from rest_framework import serializers

from .models import Comments


class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = (
            'content',
        )


class DeleteCommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ()


class ListCommentsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = (
            'id',
            'user',
            'post',
            'content',
        )
