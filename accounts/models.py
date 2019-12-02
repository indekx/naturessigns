import base64
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from core.models import Item
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    About = models.CharField(max_length=100, default='')
    phone_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.get_full_name()