from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    cat_name = models.CharField(max_length=160)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=250)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ('cat_name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return "/categories/%s/" % self.slug

    def __str__(self):
        return self.cat_name


class Article(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    slug = models.SlugField(blank=True, unique=True)
    content = models.CharField(max_length=250, null=False, blank=False)
    detail = models.TextField(null=False, blank=False, max_length=2500)
    image = models.ImageField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, through='CategoryToArticle') 

    def __str__ (self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_list')


class CategoryToArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)