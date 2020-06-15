from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Category of articles
class Category(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=160)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_articles_by_cat_url(self):
        return reverse('articles_by_category', args=[self.slug])

    def __str__(self):
        return self.title


# Articles
class Article(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, 
        on_delete=models.CASCADE, null=True,  blank=True)
    category = models.ForeignKey(Category, blank=True, 
        on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, unique=True)
    content = models.CharField(max_length=250, null=False, blank=False)
    detail = models.TextField(null=False, blank=False, max_length=2500)
    image = models.ImageField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, null=True)

    def __str__ (self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_list', args=[self.slug])