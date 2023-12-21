from rest_framework import serializers

from .models import Posts


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = (
            'title',
            'content',
            'author_id',
            'read_permission',
            'edit_permission'
        )
