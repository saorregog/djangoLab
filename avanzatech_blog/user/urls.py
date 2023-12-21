from django.urls import path

from . import views


urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name='users-list'),
    path('create/', views.UsersCreateAPIView.as_view(), name='users-create'),
    path('<int:pk>/update/', views.UsersUpdateAPIView.as_view(), name='users-update'),
    path('<int:pk>/delete/', views.UsersDeleteAPIView.as_view(), name='users-delete'),
]
