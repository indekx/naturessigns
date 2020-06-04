from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Article(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    slug = models.SlugField(blank=True, unique=True)
    content = models.CharField(max_length=250, null=False, blank=False)
    detail = models.TextField(null=False, blank=False, max_length=2500)
    image = models.ImageField(blank=True, null=True) 

    def __str__ (self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_list')