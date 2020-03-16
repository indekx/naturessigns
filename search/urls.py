from django.conf.urls import url
from .views import SearchItemView

urlpatterns = [
   url(r'^$', SearchItemView.as_view(), name='search'),
]