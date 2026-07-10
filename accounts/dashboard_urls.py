from django.urls import path
from . import dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard_redirect, name='dashboard'),
    path('admin/', dashboard_views.admin_dashboard, name='admin_dashboard'),
    path('owner/', dashboard_views.owner_dashboard, name='owner_dashboard'),
    path('tenant/', dashboard_views.tenant_dashboard, name='tenant_dashboard'),
]
