from django import forms
from . import models


class AddProduct(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
            'title',
            'category',
            'image',
            'width',
            'height',
            'description',
            'detail',
         ]
        
    login_url = '/login/' 

class ContactUsForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name'}
        ), label="", max_length=65, required=True
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name'}
        ), label="", max_length=65, required=True
    )
    contact_email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email address'}
        ), label="", max_length=254, required=True
    )

    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Message'}
        ), label="", max_length=1500, required=True 
    )
