from os import path
from django.conf.urls import url
from django.urls import path
from .views import OrderSummaryView
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^resources/$', views.email_subscribe, name='email_subscribe'),
    url(r'^services/$', views.our_services, name='our_services'),
    url(r'^how_we_do_it/$', views.how_we_do_it, name='how_we_do_it'),
    url(r'^store/product_list/$', views.order_item_list, name='marketplace'),
    url(r'^shopping_cart/order_summary/$', OrderSummaryView.as_view(), name='order_summary'),
    url(r'^products/add/$', views.add_product, name='add_product'), 
    url(r'^products/prostaright_tea/$', views.product_prostaright, name='prostaright_tea'),
    url(r'^services/drugs/$', views.drugs, name='drugs'),
    url(r'^products/(?P<slug>[\w-]+)/$', views.product, name='product_detail'),
    url(r'^add_to_cart/(?P<slug>[\w-]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(?P<slug>[\w-]+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^remove_item_from_cart/(?P<slug>[\w-]+)/$', views.remove_single_item_from_cart, 
        name='remove_single_item_from_cart'
    ),
]