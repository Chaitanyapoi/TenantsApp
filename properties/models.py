from django.db import models
from owners.models import Owner

class Property(models.Model):
    TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
        ('studio', 'Studio'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True, help_text="Comma-separated amenities")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city}"

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',') if a.strip()]

    class Meta:
        verbose_name_plural = "Properties"
