from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'property_type', 'address', 'city', 'state', 'pincode',
                  'bedrooms', 'bathrooms', 'area_sqft', 'monthly_rent', 'security_deposit',
                  'description', 'amenities', 'status', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '6'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amenities': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WiFi, Parking, Gym'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
