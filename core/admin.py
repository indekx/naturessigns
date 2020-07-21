from webbrowser import register

# Register your models here.
from django.contrib import admin

from .models import FrequentlyAskedQuestion, Item, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    pass


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


class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question', 'answer')


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(FrequentlyAskedQuestion, FrequentlyAskedQuestionAdmin)