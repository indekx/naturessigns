from django.contrib import admin
from django.contrib.auth.models import User
from . import models 


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("cat_name",)}


class CategoryToArticleInline(admin.TabularInline):
    model = models.CategoryToArticle
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CategoryToArticleInline]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)






