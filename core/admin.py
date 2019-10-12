from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item, OrderItem, Order


class ProductQSetAdmin(admin.ModelAdmin):
    display = [
        ('Description', 
           {'fields': 
               ['title', 'image', 
               'description', 'detail'
               ]
           }),
      ]

    class Meta:
        model = Item


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)