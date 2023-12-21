from rest_framework import generics, status, permissions
from rest_framework.response import Response

from base.query_set import BaseQuerySet
from .serializers import PostsCreateUpdateModelSerializer, PostsListModelSerializer, PostsRetrieveModelSerializer
from base.paginations import PostsCommentsListPagination


class PostsListAPIView(BaseQuerySet, generics.ListAPIView):
    serializer_class = PostsListModelSerializer
    pagination_class = PostsCommentsListPagination


class PostsCreateAPIView(generics.CreateAPIView):
    serializer_class = PostsCreateUpdateModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = {'errors': []}
        
        author = request.user
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if not title:
            error['errors'].append('Post must have a title.')

        if not content:
            error['errors'].append('Post must have content.')

        if error['errors']:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=author, title=title, content=content)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostsRetrieveAPIView(BaseQuerySet, generics.RetrieveAPIView):
    serializer_class = PostsRetrieveModelSerializer


class PostsUpdateAPIView(BaseQuerySet, generics.UpdateAPIView):
    serializer_class = PostsCreateUpdateModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        author = serializer.instance.author
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if not title:
            title = serializer.instance.title

        if not content:
            content = serializer.instance.content

        serializer.save(author=author, title=title, content=content)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# class PostsDeleteAPIView(generics.DestroyAPIView):
#     queryset = CustomUsers.objects.all()
#     serializer_class = UsersModelSerializer
#     permission_classes = [IsSuperuser]

#     def perform_destroy(self, instance):
#         instance.is_active = False
#         instance.save()
