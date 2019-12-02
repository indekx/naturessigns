from django.conf.urls import url
from . import views
from .views import DocumentListView


urlpatterns = [
    url(r'^upload/$', views.file_upload, name='upload'),
    url(r'^whitepapers/$', DocumentListView.as_view(), name='whitepapers'),
]