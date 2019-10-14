from django.conf.urls import url
from business import views
from .views import AdCreateView, AdvertListView

urlpatterns = [
    url(r'^ads/create/$', AdCreateView.as_view(), name='ad_create'),
    url(r'^all_products/$', AdvertListView.as_view(), name='all_ads'),
    url(r'^affilaite_member/$', views.become_an_affiliate, name='become_an_affiliate'),
    url(r'^new_distributor/$', views.become_distributor, name='become_distributor'),
    url(r'^adverts/post_ad/$', views.become_distributor, name='become_distributor'),
]
