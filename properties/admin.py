from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'city', 'property_type', 'monthly_rent', 'status']
    list_filter = ['status', 'property_type', 'city']
    search_fields = ['title', 'city', 'owner__full_name']
