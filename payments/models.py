from django.db import models
from tenants.models import Lease

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
    ]
    TYPE_CHOICES = [
        ('rent', 'Monthly Rent'),
        ('deposit', 'Security Deposit'),
        ('maintenance', 'Maintenance'),
        ('penalty', 'Penalty'),
        ('refund', 'Deposit Refund'),
    ]

    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='rent')
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField()
    due_date = models.DateField()
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.receipt_number} - {self.lease.tenant.full_name}"

    def total_amount(self):
        return self.amount + self.late_fee

    class Meta:
        ordering = ['-payment_date']
