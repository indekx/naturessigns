from django.conf.urls import url
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    DeleteArticleView,
    CurrentUserArticleListView,
    articles_by_category
)

from articles import views

urlpatterns = [
    url(r'^article_list/$', ArticleListView.as_view(), name='blog_list'),
    url(r'^create/$', ArticleCreateView.as_view(), name='create_article'),
    # url(r'^user<str:username>', CurrentUserArticleListView.as_view(), name='user_article'),
    url(r'^(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', ArticleUpdateView.as_view(), name='article_update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', DeleteArticleView.as_view(), name='article_delete'),
    url(r'^category/(?P<slug>[\w-]+)/$', articles_by_category, name='articles_by_category'),
]