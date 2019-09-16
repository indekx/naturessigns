from django import forms
from articles import models


class AddArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = [
            'created_by',
            'title',
            'slug',
            'content',
            'detail',
         ]

