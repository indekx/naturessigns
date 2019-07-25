from django.conf.urls import url
from baseapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^resources/$', views.email_subscribe, name='email_subscribe'),
    url(r'^services/$', views.our_services, name='our_services'),
    url(r'^how_we_do_it/$', views.how_we_do_it, name='how_we_do_it'),
    url(r'^product/add/$', views.add_product, name='add_product'),
    url(r'^products/store/$', views.store, name='store'),
    url(r'^services/drugs/$', views.drugs, name='drugs'),
    url(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='product_detail'),
]