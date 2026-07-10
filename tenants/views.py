from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant, Lease
from .forms import TenantProfileForm, LeaseForm

@login_required
def create_profile(request):
    if request.user.role != 'tenant':
        return redirect(request.user.get_dashboard_url())
    if hasattr(request.user, 'tenant_profile'):
        return redirect('/dashboard/tenant/')
    if request.method == 'POST':
        form = TenantProfileForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.user = request.user
            tenant.save()
            request.user.is_profile_complete = True
            request.user.save()
            messages.success(request, 'Tenant profile created!')
            return redirect('/dashboard/tenant/')
    else:
        form = TenantProfileForm(initial={'full_name': request.user.get_full_name()})
    return render(request, 'tenants/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    tenant = get_object_or_404(Tenant, user=request.user)
    if request.method == 'POST':
        form = TenantProfileForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('/dashboard/tenant/')
    else:
        form = TenantProfileForm(instance=tenant)
    return render(request, 'tenants/edit_profile.html', {'form': form, 'tenant': tenant})

@login_required
def tenant_list(request):
    if request.user.role not in ['admin', 'owner']:
        return redirect(request.user.get_dashboard_url())
    if request.user.role == 'owner':
        tenants = Tenant.objects.filter(leases__property__owner__user=request.user).distinct()
    else:
        tenants = Tenant.objects.select_related('user').all()
    return render(request, 'tenants/list.html', {'tenants': tenants})

@login_required
def lease_list(request):
    if request.user.role == 'owner':
        leases = Lease.objects.filter(property__owner__user=request.user).select_related('tenant', 'property')
    elif request.user.role == 'tenant':
        leases = Lease.objects.filter(tenant__user=request.user).select_related('property')
    else:
        leases = Lease.objects.select_related('tenant', 'property').all()
    return render(request, 'tenants/leases.html', {'leases': leases})

@login_required
def create_lease(request):
    if request.user.role not in ['admin', 'owner']:
        return redirect(request.user.get_dashboard_url())
    if request.method == 'POST':
        form = LeaseForm(request.POST, request.FILES)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.save()
            lease.property.status = 'occupied'
            lease.property.save()
            messages.success(request, 'Lease created successfully!')
            return redirect('lease_list')
    else:
        from properties.models import Property
        form = LeaseForm()
        if request.user.role == 'owner':
            form.fields['property'].queryset = Property.objects.filter(owner__user=request.user, status='available')
    return render(request, 'tenants/create_lease.html', {'form': form})
