from django import forms
from .models import Tenant, Lease

class TenantProfileForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['full_name', 'aadhaar_number', 'occupation', 'employer', 'monthly_income',
                  'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '12'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'employer': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'property', 'start_date', 'end_date', 'monthly_rent',
                  'security_deposit', 'deposit_paid', 'notes']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-select'}),
            'property': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
