# DJANGO IMPORTS
from django.shortcuts import get_object_or_404
from django.db.models import Q

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# MODELS
from likes.models import Likes
from comments.models import Comments

# QUERY SET
from base.query_set import BasePostsQuerySet

# SERIALIZERS
from .serializers import PostsCreateUpdateModelSerializer, PostsListModelSerializer, PostsRetrieveModelSerializer, PostsDeleteModelSerializer
from likes.serializers import LikeModelSerializer, ListLikesModelSerializer
from comments.serializers import CommentModelSerializer, ListCommentsModelSerializer, DeleteCommentModelSerializer

# PAGINATION
from base.paginations import ListPostsCommentsPagination, ListLikesPagination


class PostsListAPIView(BasePostsQuerySet, generics.ListAPIView):
    '''
    It shows all the posts on the blogging platform, according to the read permission of each post
    '''
    serializer_class = PostsListModelSerializer
    pagination_class = ListPostsCommentsPagination


class PostsRetrieveAPIView(BasePostsQuerySet, generics.RetrieveAPIView):
    '''
    It shows the specified post (path param) on the blogging platform, according to the read permission of the post
    '''
    serializer_class = PostsRetrieveModelSerializer


class PostsCreateAPIView(generics.CreateAPIView):
    '''
    It creates a new post on the blogging platform with configurable read/edit permissions, but only if the user is authenticated
    '''
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

        serializer.save(author=author)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostsUpdateAPIView(BasePostsQuerySet, generics.UpdateAPIView):
    '''
    It edits the specified post (path param) on the blogging platform, but only if the user is authenticated and according to the edit permission of the post
    '''
    serializer_class = PostsCreateUpdateModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if not title:
            title = serializer.instance.title

        if not content:
            content = serializer.instance.content

        serializer.save(title=title, content=content)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PostsDeleteAPIView(BasePostsQuerySet, generics.DestroyAPIView):
    '''
    It deletes (soft delete) the specified post (path param) on the blogging platform, but only if the user is authenticated and according to the edit permission of the post
    '''
    serializer_class = PostsDeleteModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostsListLikesAPIView(BasePostsQuerySet, generics.ListAPIView):
    '''
    It shows all the likes linked to the specified post (path param) on the blogging platform, according to the read permission of each post
    '''
    serializer_class = ListLikesModelSerializer
    pagination_class = ListLikesPagination

    def list(self, request, *args, **kwargs):
        post = self.get_object()

        likes = Likes.objects.filter(Q(post=post) & Q(is_active=True))

        page = self.paginate_queryset(likes)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(likes, many=True)

        return Response(serializer.data)


class PostsLikeAPIView(BasePostsQuerySet, generics.CreateAPIView):
    '''
    It creates/deletes (soft delete) a like linked to the specified post (path param) on the blogging platform, but only if the user is authenticated and according to the read permission of the post
    '''
    serializer_class = LikeModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post = self.get_object()

        like, created = Likes.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.is_active = not like.is_active
            like.save()

        return Response(status=status.HTTP_200_OK)


class PostsListCommentsAPIView(BasePostsQuerySet, generics.ListAPIView):
    '''
    It shows all the comments linked to the specified post (path param) on the blogging platform, according to the read permission of each post
    '''
    serializer_class = ListCommentsModelSerializer
    pagination_class = ListPostsCommentsPagination

    def list(self, request, *args, **kwargs):
        post = self.get_object()

        comments = Comments.objects.filter(Q(post=post) & Q(is_active=True))

        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comments, many=True)

        return Response(serializer.data)


class PostsCommentAPIView(BasePostsQuerySet, generics.CreateAPIView):
    '''
    It creates a comment linked to the specified post (path param) on the blogging platform, but only if the user is authenticated and according to the read permission of the post
    '''
    serializer_class = CommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = {'errors': []}
        
        user = request.user
        content = serializer.validated_data.get('content')

        if not content:
            error['errors'].append('Comments must have content.')

        if error['errors']:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user, post=post)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class PostsDeleteCommentAPIView(BasePostsQuerySet, generics.DestroyAPIView):
    '''
    It deletes (soft delete) the specified comment (query param) linked to the specified post (path param) on the blogging platform; but only if the user is authenticated and the comment's owner (in case the user is a blogger), and according to the read permission of the post
    '''
    serializer_class = DeleteCommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        comment_pk = self.request.query_params.get('comment_id')

        if not comment_pk:
            error = {'errors': ['No query param in the URL (comment_id).']}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role == 'admin':
            comment = get_object_or_404(Comments, Q(pk=comment_pk) & Q(post=post))
        
        if request.user.role == 'blogger':
            comment = get_object_or_404(Comments, Q(pk=comment_pk) & Q(user=request.user) & Q(post=post))

        comment.is_active = False
        comment.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
