import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, query, signals
from django.db.models.signals import pre_save
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy

from purchase.models import BillingAddress


class Item(models.Model):
    CAT_CHOICES = (
        ( '', 'select' ),
        ('BEAUTY', 'Beauty'),
        ('PERSONAL_CARE', 'Personal Care'),
        ('MEDICINE_AND_TREATMENT', 'Medicine & Treatment'),
        ('NATURAL_AND_ORGANIC', 'Natural & Organic'),
        ('SUPPLEMENT_AND_VITAMINS', 'Supplements & Vitamins'),
    )    

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
    category = models.CharField(choices=CAT_CHOICES, default='select', max_length=20)
    label = models.CharField(choices=LABEL_CHOICES, max_length=15, default='select')
    description = models.TextField(blank=False, max_length=3000)
    additional_information = models.TextField(blank=True, max_length=3000)
    slug = models.SlugField()
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs = {
        'slug': self.slug
    })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs = {
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
        return f"{self.quantity} of {self.item.title}"
    
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
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_sum_total(self):
        sum_total = 0
        for order_item in self.items.all():
            sum_total += order_item.get_final_price()
        return sum_total