from django.urls import path

from . import views


urlpatterns = [
    path('', views.PostsListAPIView.as_view(), name='posts-list'),
    path('create/', views.PostsCreateAPIView.as_view(), name='posts-create'),
    path('<int:pk>/', views.PostsRetrieveAPIView.as_view(), name='posts-retrieve'),
    path('update/<int:pk>/', views.PostsUpdateAPIView.as_view(), name='posts-update'),
    # path('delete/<int:pk>/', views.PostsDeleteAPIView.as_view(), name='posts-delete'),
]
