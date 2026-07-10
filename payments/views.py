from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Payment
from .forms import PaymentForm, TenantPaymentForm
from tenants.models import Lease


@login_required
def payment_list(request):
    if request.user.role == 'owner':
        payments = Payment.objects.filter(
            lease__property__owner__user=request.user
        ).select_related('lease__tenant', 'lease__property')
    elif request.user.role == 'tenant':
        payments = Payment.objects.filter(
            lease__tenant__user=request.user
        ).select_related('lease__property')
    else:
        payments = Payment.objects.select_related(
            'lease__tenant', 'lease__property'
        ).all()

    # Summary totals for the current user's scope
    total_paid    = payments.filter(status='completed').aggregate(t=Sum('amount'))['t'] or 0
    total_pending = payments.filter(status='pending').aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'payments':      payments,
        'total_paid':    total_paid,
        'total_pending': total_pending,
    }
    return render(request, 'payments/list.html', context)


@login_required
def create_payment(request):
    """Owner / Admin: full payment form."""
    if request.user.role not in ['admin', 'owner']:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment recorded successfully!')
            return redirect('payment_list')
    else:
        form = PaymentForm()
        if request.user.role == 'owner':
            form.fields['lease'].queryset = Lease.objects.filter(
                property__owner__user=request.user
            )

    return render(request, 'payments/create.html', {'form': form})


@login_required
def tenant_make_payment(request):
    """Tenant: submit a payment against their active lease."""
    if request.user.role != 'tenant':
        return redirect(request.user.get_dashboard_url())

    # Tenants must have an active lease to pay
    try:
        tenant = request.user.tenant_profile
    except Exception:
        messages.error(request, 'Please complete your tenant profile first.')
        return redirect('/tenants/profile/create/')

    lease = tenant.active_lease()
    if not lease:
        messages.warning(request, 'You have no active lease to make a payment against.')
        return redirect('payment_list')

    if request.method == 'POST':
        form = TenantPaymentForm(request.POST, lease=lease)
        if form.is_valid():
            payment = form.save(commit=True, lease=lease, user=request.user)
            messages.success(
                request,
                f'Payment of ₹{payment.amount} submitted (Receipt: {payment.receipt_number}). '
                'Status is pending until confirmed by your owner.'
            )
            return redirect('payment_list')
    else:
        form = TenantPaymentForm(lease=lease)

    context = {
        'form':  form,
        'lease': lease,
    }
    return render(request, 'payments/tenant_pay.html', context)


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payments/detail.html', {'payment': payment})
