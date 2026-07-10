from django.db import models
from accounts.models import User

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    full_name = models.CharField(max_length=200)
    aadhaar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    pan_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Owner: {self.full_name}"

    def total_properties(self):
        return self.properties.count()

    def total_income(self):
        from payments.models import Payment
        return Payment.objects.filter(
            lease__property__owner=self, status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
