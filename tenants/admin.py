from django.contrib import admin
from .models import Tenant, Lease

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'occupation', 'employer']

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property', 'start_date', 'end_date', 'status', 'monthly_rent']
    list_filter = ['status']
