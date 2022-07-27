from payment.views import pay_for_order, success, unsuccessful, check_unitpay
from django.urls import path
from django.urls import include
from django.conf.urls import url
from payment.paysera import check_paysera_payment_status

urlpatterns = [
    path('payment/<int:order_id>/', pay_for_order, name='payment'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path('success/', success, name='successfully_payment'),
    path('unsuccessful/', unsuccessful, name='unsuccessful_payment'),
    path('check_unitpay/', check_unitpay),
    path('check_paysera/', check_paysera_payment_status),
]