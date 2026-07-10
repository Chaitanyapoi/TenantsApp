from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Owner
from .forms import OwnerProfileForm

@login_required
def create_profile(request):
    if request.user.role != 'owner':
        return redirect(request.user.get_dashboard_url())
    if hasattr(request.user, 'owner_profile'):
        return redirect('/dashboard/owner/')
    if request.method == 'POST':
        form = OwnerProfileForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = request.user
            owner.save()
            request.user.is_profile_complete = True
            request.user.save()
            messages.success(request, 'Owner profile created successfully!')
            return redirect('/dashboard/owner/')
    else:
        form = OwnerProfileForm(initial={'full_name': request.user.get_full_name()})
    return render(request, 'owners/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    owner = get_object_or_404(Owner, user=request.user)
    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('/dashboard/owner/')
    else:
        form = OwnerProfileForm(instance=owner)
    return render(request, 'owners/edit_profile.html', {'form': form, 'owner': owner})

@login_required
def owner_list(request):
    if not request.user.is_staff:
        return redirect(request.user.get_dashboard_url())
    owners = Owner.objects.select_related('user').all()
    return render(request, 'owners/list.html', {'owners': owners})
