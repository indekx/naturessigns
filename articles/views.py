from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
def blog_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'blog/view_blog.html', {'articles': articles})


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'blog/blog_detail.html', {'article': article})


@login_required(login_url='/accounts/login/')
def create_article(request):
    form = forms.AddArticle()
    
    return render(request, 'blog/create_article.html', {'form': form})

