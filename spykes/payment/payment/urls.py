from django.urls import path
from payment.views import pay_view, pay_confirm_view

urlpatterns = [
    path('pay', pay_view, name='pay_view'),
    path('pay/confirm', pay_confirm_view, name='pay_confirm_view'),
]
