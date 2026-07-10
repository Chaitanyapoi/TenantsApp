from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'lease', 'amount', 'payment_type', 'status', 'payment_date']
    list_filter = ['status', 'payment_type', 'payment_method']
