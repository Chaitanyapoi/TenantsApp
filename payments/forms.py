from django import forms
from .models import Payment
from tenants.models import Lease
import random, string


class PaymentForm(forms.ModelForm):
    """Full payment form for owners and admins."""
    class Meta:
        model = Payment
        fields = ['lease', 'amount', 'payment_type', 'payment_method', 'status',
                  'payment_date', 'due_date', 'transaction_id', 'late_fee', 'notes']
        widgets = {
            'lease':          forms.Select(attrs={'class': 'form-select'}),
            'amount':         forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_type':   forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'status':         forms.Select(attrs={'class': 'form-select'}),
            'payment_date':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'late_fee':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.receipt_number:
            instance.receipt_number = 'RCP-' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        if commit:
            instance.save()
        return instance


class TenantPaymentForm(forms.ModelForm):
    """
    Simplified payment form for tenants — they can only pay against
    their own active lease and cannot change status or late_fee.
    """
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type', 'payment_method', 'payment_date',
                  'due_date', 'transaction_id', 'notes']
        widgets = {
            'amount':         forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_type':   forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_date':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UPI Ref / Bank Ref / Cheque No. (optional)',
            }),
            'notes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2,
                                                    'placeholder': 'Any additional notes…'}),
        }

    def __init__(self, *args, lease=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill amount from lease if available
        if lease:
            self.lease = lease
            self.fields['amount'].initial = lease.monthly_rent
        # Tenants can only pay rent or deposit
        self.fields['payment_type'].choices = [
            ('rent',    'Monthly Rent'),
            ('deposit', 'Security Deposit'),
            ('maintenance', 'Maintenance Charge'),
        ]

    def save(self, commit=True, lease=None, user=None):
        instance = super().save(commit=False)
        instance.lease = lease
        instance.status = 'pending'   # pending until owner confirms
        instance.late_fee = 0
        if not instance.receipt_number:
            instance.receipt_number = 'RCP-' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        if commit:
            instance.save()
        return instance
