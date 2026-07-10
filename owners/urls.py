from django.urls import path
from . import views

urlpatterns = [
    path('profile/create/', views.create_profile, name='owner_create_profile'),
    path('profile/edit/', views.edit_profile, name='owner_edit_profile'),
    path('list/', views.owner_list, name='owner_list'),
]
