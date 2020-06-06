from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, 
    DeleteView
)
   
from .models import Article, Category
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    ordering = ['-date']
    paginate_by = 3


class CurrentUserArticleListView(ListView):
    model = Article
    template_name = 'blog/user_blog_posts.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(created_by=user).ordering('-date')


class ArticleDetailView(DetailView):
    queryset = Article.objects.all() # Same as using 'model' which is 'Article'
    template_name = 'blog/article_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)


def article_by_category(request, category_slug, selected_page=1):
    # Get specified category
    articles = Article.objects.all().order_by('-date')
    category_articles = []
    for article in articles:
        if article.categories.filter(slug=category_slug):
            category_articles.append(article)
    # Paginate the categories
    by_cat_pages = Paginator(articles, 5)
    # Get articles by categories
    get_articles_by_cats = Category.objects.filter(slug=category_slug)[0]
    # Get specified page
    try:
        returned_cat_page = by_cat_pages.by_cat_page(selected_page)
    except  EmptyPage:
        returned_cat_page = get_articles_by_cats.by_cat_page(by_cat_pages.num_by_cat_pages)
    # Display all the articles
    return render(request, 'blog/articles_by_cats.html', {
            'articles': returned_cat_page.object_list,
            'by_cat_page': returned_cat_page,
            'get_articles_by_cats': get_articles_by_cats
        }
    )



class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_form.html'
    fields = [
        'title', 'content', 'detail', 'slug'
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'blog/article_form.html'
    fields = [
        'title', 'content', 'detail', 'slug'
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        
        if self.request.user == article.created_by:
            return True
        else:
            return False

    
class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = '/articles/article_list/'

    def test_func(self):
        article = self.get_object()
        
        if self.request.user == article.created_by:
            return True
        else:
            return False