from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from properties.models import Property
from tenants.models import Tenant, Lease
from payments.models import Payment
from accounts.models import User

@login_required
def dashboard_redirect(request):
    from django.shortcuts import redirect
    return redirect(request.user.get_dashboard_url())

@login_required
def admin_dashboard(request):
    if not request.user.is_staff and request.user.role != 'admin':
        from django.shortcuts import redirect
        return redirect(request.user.get_dashboard_url())
    context = {
        'total_users': User.objects.count(),
        'total_properties': Property.objects.count(),
        'total_tenants': Tenant.objects.count(),
        'total_revenue': Payment.objects.filter(status='completed').aggregate(t=Sum('amount'))['t'] or 0,
        'recent_payments': Payment.objects.select_related('lease__tenant', 'lease__property').order_by('-created_at')[:5],
        'available_properties': Property.objects.filter(status='available').count(),
        'occupied_properties': Property.objects.filter(status='occupied').count(),
    }
    return render(request, 'shared/admin_dashboard.html', context)

@login_required
def owner_dashboard(request):
    if request.user.role != 'owner':
        from django.shortcuts import redirect
        return redirect(request.user.get_dashboard_url())
    try:
        owner = request.user.owner_profile
        properties = owner.properties.all()
        leases = Lease.objects.filter(property__owner=owner)
        payments = Payment.objects.filter(lease__property__owner=owner)
        context = {
            'owner': owner,
            'properties': properties,
            'total_properties': properties.count(),
            'occupied': properties.filter(status='occupied').count(),
            'available': properties.filter(status='available').count(),
            'total_income': payments.filter(status='completed').aggregate(t=Sum('amount'))['t'] or 0,
            'active_leases': leases.filter(status='active').count(),
            'recent_payments': payments.order_by('-created_at')[:5],
        }
    except:
        from django.shortcuts import redirect
        return redirect('/owners/profile/create/')
    return render(request, 'shared/owner_dashboard.html', context)

@login_required
def tenant_dashboard(request):
    if request.user.role != 'tenant':
        from django.shortcuts import redirect
        return redirect(request.user.get_dashboard_url())
    try:
        tenant = request.user.tenant_profile
        lease = tenant.active_lease()
        payments = Payment.objects.filter(lease__tenant=tenant) if lease else Payment.objects.none()
        context = {
            'tenant': tenant,
            'lease': lease,
            'total_paid': payments.filter(status='completed').aggregate(t=Sum('amount'))['t'] or 0,
            'pending_payments': payments.filter(status='pending').count(),
            'recent_payments': payments.order_by('-created_at')[:5],
        }
    except:
        from django.shortcuts import redirect
        return redirect('/tenants/profile/create/')
    return render(request, 'shared/tenant_dashboard.html', context)
