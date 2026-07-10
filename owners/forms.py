from django import forms
from .models import Owner

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'aadhaar_number', 'pan_number', 'bank_account', 'ifsc_code', 'emergency_contact']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '12'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
