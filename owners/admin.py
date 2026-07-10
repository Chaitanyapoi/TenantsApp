from django.contrib import admin
from .models import Owner

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'pan_number', 'total_properties']
    search_fields = ['full_name', 'user__email']
