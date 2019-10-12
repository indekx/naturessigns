from django.conf.urls import url
from accounts.urls import urlpatterns
from .views import OrderPaymentView
from . import views

urlpatterns = [
    url(r'^confirm_my_order/', OrderPaymentView.as_view(), name='proceed_to_pay'),
]
