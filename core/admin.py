from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item, OrderItem, Order, Category

class ItemAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'cat_name', 'slug',
    )
    prepopulated_fields = {
        'slug':('cat_name',)
    }

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


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)