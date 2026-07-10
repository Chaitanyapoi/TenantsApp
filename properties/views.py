from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Property
from .forms import PropertyForm

@login_required
def property_list(request):
    # --- Search / Filter params ---
    city_query   = request.GET.get('city', '').strip()
    type_filter  = request.GET.get('type', '').strip()
    min_rent     = request.GET.get('min_rent', '').strip()
    max_rent     = request.GET.get('max_rent', '').strip()
    beds_filter  = request.GET.get('bedrooms', '').strip()

    if request.user.role == 'owner':
        properties = Property.objects.filter(owner__user=request.user)
    elif request.user.role == 'tenant':
        properties = Property.objects.filter(status='available')
    else:
        properties = Property.objects.select_related('owner').all()

    # Apply filters (tenants + admin; owners only see their own so city search still useful)
    if city_query:
        properties = properties.filter(
            Q(city__icontains=city_query) | Q(state__icontains=city_query) | Q(pincode__icontains=city_query)
        )
    if type_filter:
        properties = properties.filter(property_type=type_filter)
    if min_rent:
        try:
            properties = properties.filter(monthly_rent__gte=float(min_rent))
        except ValueError:
            pass
    if max_rent:
        try:
            properties = properties.filter(monthly_rent__lte=float(max_rent))
        except ValueError:
            pass
    if beds_filter:
        try:
            properties = properties.filter(bedrooms=int(beds_filter))
        except ValueError:
            pass

    # Distinct cities for the datalist autocomplete
    all_cities = Property.objects.values_list('city', flat=True).distinct().order_by('city')

    context = {
        'properties': properties,
        'all_cities': all_cities,
        'city_query': city_query,
        'type_filter': type_filter,
        'min_rent': min_rent,
        'max_rent': max_rent,
        'beds_filter': beds_filter,
        'result_count': properties.count(),
        'property_types': Property.TYPE_CHOICES,
    }
    return render(request, 'properties/list.html', context)


@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/detail.html', {'property': property})


@login_required
def create_property(request):
    if request.user.role != 'owner':
        return redirect(request.user.get_dashboard_url())
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user.owner_profile
            prop.save()
            messages.success(request, 'Property added successfully!')
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/create.html', {'form': form})


@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner__user=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated!')
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/edit.html', {'form': form, 'property': property})


@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner__user=request.user)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted.')
        return redirect('property_list')
    return render(request, 'properties/confirm_delete.html', {'property': property})
