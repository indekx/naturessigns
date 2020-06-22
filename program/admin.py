from django.contrib import admin
from . import models 


class PartnerJoinAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country',)


class SellApplyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'product_name', 'country_of_residence',)  


admin.site.register(models.PartnerJoin, PartnerJoinAdmin)
admin.site.register(models.SellApply, SellApplyAdmin)