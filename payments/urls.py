from django.urls import path
from . import views

urlpatterns = [
    path('',           views.payment_list,          name='payment_list'),
    path('create/',    views.create_payment,         name='create_payment'),
    path('pay/',       views.tenant_make_payment,    name='tenant_make_payment'),
    path('<int:pk>/',  views.payment_detail,         name='payment_detail'),
]
