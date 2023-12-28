from django.urls import path

from . import views


urlpatterns = [
    path('', views.PostsListAPIView.as_view(), name='posts-list'),
    path('create/', views.PostsCreateAPIView.as_view(), name='posts-create'),
    path('<int:pk>/', views.PostsRetrieveAPIView.as_view(), name='posts-retrieve'),
    path('update/<int:pk>/', views.PostsUpdateAPIView.as_view(), name='posts-update'),
    path('like/<int:pk>/', views.PostsLikeAPIView.as_view(), name='posts-like'),
    path('list_likes/<int:pk>/', views.PostsListLikesAPIView.as_view(), name='posts-list_likes'),
    path('comment/<int:pk>/', views.PostsCommentAPIView.as_view(), name='posts-comment'),
    path('comment/delete/<int:pk>/', views.PostsDeleteCommentAPIView.as_view(), name='posts-delete_comment'),
    path('list_comments/<int:pk>/', views.PostsListCommentsAPIView.as_view(), name='posts-list_comments'),
    path('delete/<int:pk>/', views.PostsDeleteAPIView.as_view(), name='posts-delete'),
]
