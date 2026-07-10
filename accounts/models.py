from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Property Owner'),
        ('tenant', 'Tenant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_dashboard_url(self):
        role_urls = {
            'admin': '/dashboard/admin/',
            'owner': '/dashboard/owner/',
            'tenant': '/dashboard/tenant/',
        }
        return role_urls.get(self.role, '/dashboard/')
