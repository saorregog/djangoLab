# DJANGO IMPORTS
from django.urls import path

# VIEWS
from . import views


urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name='users-list'),
    path('create/', views.UsersCreateAPIView.as_view(), name='users-create'),
    path('update/<int:pk>/', views.UsersUpdateAPIView.as_view(), name='users-update'),
    path('delete/<int:pk>/', views.UsersDeleteAPIView.as_view(), name='users-delete'),
]
