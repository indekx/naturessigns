import uuid

from django.conf import settings
from . import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, query, signals
from django.db.models.signals import pre_save
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy

from decimal import Decimal

CATEGORY_CHOICES = (
    ('', 'select'),
    ('ORG', 'Organic Formulations'),
    ('BODY CARE', 'Body Care')
)


class ItemQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def featured(self):
        return self.filter(featured=True, active=True)
    
    def search(self, query):
        lookups = (
                   Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) 
                  )
        return self.filter(lookups).distinct()


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)


class Item(models.Model):

    LABEL_CHOICES = (
        ('', 'select'),
        ('P', 'primary'),
        ('S', 'secondary'),
        ('D', 'danger'),
    )
    
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=False, default=None, null=False)
    price = models.DecimalField(blank=False, null=False, default=None, max_digits=19, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, default=None, max_digits=19, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, default='select', max_length=20, null=True, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=15, default='select')
    description = models.TextField(blank=False, max_length=3000)
    featured = models.BooleanField(default=False)
    acitve = models.BooleanField(default=False)
    additional_information = models.TextField(blank=True, max_length=3000)
    slug = models.SlugField()
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = ItemManager()

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs = {
        'slug': self.slug
    })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
        'slug': self.slug
    })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs = {
        'slug': self.slug
    })
    
        
    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
            default=None, blank=True, null=True
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
 
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()
        
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()
            


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
            default=None, blank=True, null=True
    )
    start_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_sum_total(self):
        sum_total = 0
        for order_item in self.items.all():
            sum_total += order_item.get_final_price()
        return sum_total

    def get_vat(self):
        return Decimal('7.50')/Decimal(100) * self.get_sum_total()

    def get_amount_payable(self):
        return self.get_sum_total() + self.get_vat()


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


class FrequentlyAskedQuestion(models.Model):
    topic = models.CharField(max_length=120, blank=True)
    question = models.CharField(max_length=120)
    answer = models.TextField(max_length=3500)

    class Meta:
        verbose_name = 'Frequently Asked Question'
        verbose_name_plural = 'Frequently Asked Questions'

    def __str__(self):
        return self.question