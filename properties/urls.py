from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('create/', views.create_property, name='create_property'),
    path('<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('<int:pk>/delete/', views.delete_property, name='delete_property'),
]
