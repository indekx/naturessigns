from django.contrib import admin
from django.contrib.auth.models import User
from . import models 


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'published', 'status','category')
    list_filter = ('status', 'created_on', 'published', 'created_by', 'category')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content')
    

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)






