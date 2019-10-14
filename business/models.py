from random import choices
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

CAT_CHOICES = (
    ( '', 'select' ),
    ('BEAUTY', 'Beauty'),
    ('PERSONAL_CARE', 'Personal Care'),
    ('MEDICINE_AND_TREATMENT', 'Medicine & Treatment'),
    ('NATURAL_AND_ORGANIC', 'Natural & Organic'),
    ('SUPPLEMENT_AND_VITAMINS', 'Supplements & Vitamins'),
)


class Advert(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    image = models.ImageField(null=False, blank=False, default=None)
    price = models.DecimalField(blank=False, null=False, default=None, max_digits=19, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, default=None, max_digits=19, decimal_places=2)
    category = models.CharField(choices=CAT_CHOICES, default='select', max_length=20)
    slug = models.SlugField(blank=True, unique=True)
    description = models.CharField(max_length=250, null=False, blank=False)
    detail = models.TextField(null=False, blank=False, max_length=2500)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
    

    def __str__ (self):
        return self.label

    def get_absolute_url(self):
        return reverse('ad_list')


#Affiliate Program Model
LEVELS = (
    ('', 'select'),
    ('Manufacturer', 'Manufacturer'),
    ('Wholesaler', 'Wholesaler'),
)

class BecomeAnAffiliate(models.Model):
    
    first_name = models.CharField(blank=False, max_length=60)
    last_name = models.CharField(blank=False, max_length=60)
    email = models.EmailField(blank=False)
    job_title = models.CharField(blank=False, max_length=50)
    contact_phone_number = models.CharField(blank=False, max_length=15)
    tell_us_about_you = models.CharField(choices=LEVELS, default='select', blank=False, max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    contact_address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=70, blank=True)
    state = models.CharField(max_length=70, blank=True)
    country = models.CharField(max_length=120, blank=True)
    website = models.CharField(max_length=100, blank=False)

