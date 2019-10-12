from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from . import forms 


# Create your models here.
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address_line_1 = models.CharField(max_length=255)
    shipping_address_line_2 = models.CharField(max_length=255)
    state = models.CharField(choices=forms.STATES, max_length=55)
    phone_number = models.CharField(blank=False, null=False, default=None, max_length=15)
    zip_code = models.CharField(blank=True, max_length=6)
    same_as_shipping_address = models.BooleanField(blank=True, null=True)
    save_info = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.user.username