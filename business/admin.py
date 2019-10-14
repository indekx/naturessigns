from django.contrib import admin
from .models import BecomeAnAffiliate, Advert


class BecomeAnAffiliateAdmin(admin.ModelAdmin):
    display = [
        ('Description', 
           {'fields': 
               ['first_name', 'last_name', 
               'email', 'job_title',
               'contact_phone_number',
               'tell_us_about_you',
               'company_name',
               'contact_address',
               'city ', 'state',
               'country', 'website',
               ]
           }),
      ]

    class Meta:
        model = BecomeAnAffiliate

admin.site.register(Advert)

