from django.urls import path
from . import views

urlpatterns = [
    path('profile/create/', views.create_profile, name='tenant_create_profile'),
    path('profile/edit/', views.edit_profile, name='tenant_edit_profile'),
    path('list/', views.tenant_list, name='tenant_list'),
    path('leases/', views.lease_list, name='lease_list'),
    path('leases/create/', views.create_lease, name='create_lease'),
]
