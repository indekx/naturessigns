from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^partner/$', views.partner_program_view, name='partner'),
    url(r'^partner_register/$', views.partner_interest_view, name='partner_register'),
    url(r'^partner_register/success/$', views.partner_reg_success, name='partner_register_success'),
    url(r'^sell/apply/$', views.sell_apply_view, name='sell_apply'),
    url(r'^sell/apply/success/$', views.sell_apply_success, name='sell_apply_success'),
]