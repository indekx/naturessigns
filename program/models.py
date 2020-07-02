from django.db import models
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


# Join affiliate model
PRODUCT_TYPE_CHOICES = (
    ('', 'select'),
    ('supplements & vitamins', 'Supplements & Vitamins'),
    ('beauty', 'Beauty'),
    ('body care', 'Body Care'),
    ('herbal supplements', 'Herbal Supplements'),
    ('conditioners', 'Conditioners'),
    ('nutritions', 'Nutritions'),
)
BUSINESS_CATEGORY_CHOICES = (
    ('', 'select'),
    ('manu', 'Manufacturing'),
    ('packaging', 'Packaging'),
    ('retailer', 'Retail'),
    ('marketing', 'Marketing & Supplies')
)

class PartnerJoin(models.Model):
    full_name = models.CharField(max_length=60)
    email_address = models.EmailField()
    company_or_business_name = models.CharField(max_length=255)
    business_address_line_1 = models.CharField(max_length=512)
    business_address_line_2 = models.CharField(
        max_length=512, blank=True, null=True)
    state_or_province = models.CharField(max_length=255)
    country = CountryField()
    zip_code = models.CharField(blank=True, null=True, max_length=7)
    business_phone_number = models.CharField(
        max_length=19, blank=True, null=True)
    website = models.CharField(max_length=160, null=True, blank=True)
    product_type = models.CharField(
        choices=PRODUCT_TYPE_CHOICES, default='select', max_length=255)
    product_features_and_benefits = models.TextField(max_length=2500)
    business_category = models.CharField(
        choices=BUSINESS_CATEGORY_CHOICES, default='select', max_length=200)

    def __str__(self):
        return self.email_address


# Intent to sell model
class SellApply(models.Model):
    full_name = models.CharField(max_length=60)
    email = models.EmailField()
    phone_number = models.CharField(max_length=19, blank=True, null=True)
    country_of_citizenship = CountryField()
    country_of_residence = CountryField()
    product_origin = CountryField()
    product_name = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=120, blank=True)
    date_produced = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    selling_price = models.CharField(blank=False, null=False, max_length=19)
    # image = models.ImageField(blank=False, default=None, null=True)
    product_description = models.TextField(max_length=1500)

    class Meta:
        verbose_name = 'Sell Item Application'
        verbose_name_plural = 'Sell Item Applications'

    def __str__(self):
        return self.product_name


# Distributor
GENDER_CHOICES = (
    ('', 'select'),
    ('f', 'female'),
    ('m', 'male')
)
WORK_AS_CHOICES = (
    ('', 'select'),
    ('company', 'Company'),
    ('individual', 'Individual')
)
DEMAND_CHOICES = (
    ('', 'select'),
    ('low', 'Low'),
    ('self high', 'High'),
)
MEDIA_TYPE_CHOICES = (
    ('internet', 'Internet'),
    ('newspaper', 'Newspaper'),
    ('facebook', 'Facebook'),
    ('google', 'Google'),
)
class BecomeDistributor(models.Model):
 
    full_name = models.CharField(max_length=60)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=8)
    contact_address = models.CharField(max_length=1500)
    phone_number = models.CharField(max_length=19, null=True)
    i_apply_as = models.CharField(choices=WORK_AS_CHOICES, max_length=19, default='select')
    weekly_sales_qty = models.IntegerField(null=True, default=2)
    medium = MultiSelectField(choices=MEDIA_TYPE_CHOICES, max_choices=3, default=None)

    class Meta:
        verbose_name = 'Distributor Application'
        verbose_name_plural = 'Distributor Applications'   

    def __str__(self):
        return self.full_name
