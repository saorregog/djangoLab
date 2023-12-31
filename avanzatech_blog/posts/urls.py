# DJANGO IMPORTS
from django.urls import path

# VIEWS
from . import views


urlpatterns = [
    # posts
    path('', views.PostsListAPIView.as_view(), name='posts-list'),
    path('<int:pk>/', views.PostsRetrieveAPIView.as_view(), name='posts-retrieve'),
    path('create/', views.PostsCreateAPIView.as_view(), name='posts-create'),
    path('update/<int:pk>/', views.PostsUpdateAPIView.as_view(), name='posts-update'),
    path('delete/<int:pk>/', views.PostsDeleteAPIView.as_view(), name='posts-delete'),

    # likes
    path('list_likes/<int:pk>/', views.PostsListLikesAPIView.as_view(), name='posts-list_likes'),
    path('like/<int:pk>/', views.PostsLikeAPIView.as_view(), name='posts-like'),

    # comments
    path('list_comments/<int:pk>/', views.PostsListCommentsAPIView.as_view(), name='posts-list_comments'),
    path('comment/<int:pk>/', views.PostsCommentAPIView.as_view(), name='posts-comment'),
    path('comment/delete/<int:pk>/', views.PostsDeleteCommentAPIView.as_view(), name='posts-delete_comment'),
]
