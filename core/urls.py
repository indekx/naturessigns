from os import path
from django.conf.urls import url
from django.urls import path
from .views import OrderSummaryView, OrderCheckoutView
from core import views
from core.views import index_view

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^about/mission/$', views.our_mission, name='our_mission'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^how_to_buy/$', views.how_to_buy, name='how_to_buy'),
    url(r'^health/enlarged_prostate/$', views.enlarged_prostate_view, name='enlarged_prostate'),
    url(r'^resources/$', views.email_subscribe, name='email_subscribe'),
    url(r'^services/$', views.our_services, name='our_services'),
    url(r'^legal/privacy_policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^legal/cookie_policy/$', views.cookie_policy, name='cookie_policy'),
    url(r'^legal/disclaimer/$', views.disclaimer, name='disclaimer'),
    url(r'^protection/return_policy/$', views.return_policy, name='return_policy'),
    url(r'^legal/terms_and_conditions/$', views.terms_and_conditions, name='terms_and_conditions'),
    url(r'^how_we_do_it/$', views.how_we_do_it, name='how_we_do_it'),
    url(r'^store/product_list/$', views.order_item_list, name='marketplace'),
    url(r'^shopping_cart/order_summary/$', OrderSummaryView.as_view(), name='order_summary'),
    url(r'^products/add/$', views.add_product, name='add_product'), 
    url(r'^products/prostaright_tea/$', views.product_prostaright, name='prostaright_tea'),
    url(r'^services/drugs/$', views.drugs, name='drugs'),
    url(r'^checkout/', OrderCheckoutView.as_view(), name='proceed_to_pay'),
    url(r'^products/category/(?P<category_slug>[\w-]+)/$', views.item_category_view, name="items_by_category"),
    url(r'^products/category_detail/(?P<category_slug>[\w-]+)/$', views.cat_detail_view, name='category_detail'),
    url(r'^products/(?P<slug>[\w-]+)/$', views.product, name='product_detail'),
    url(r'^add_to_cart/(?P<slug>[\w-]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(?P<slug>[\w-]+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^remove_item_from_cart/(?P<slug>[\w-]+)/$', views.remove_single_item_from_cart, 
        name='remove_single_item_from_cart'
        ),
]