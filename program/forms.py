from django import forms
from .models import PartnerJoin, SellApply

from phonenumber_field.formfields import PhoneNumberField
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


class PartnerJoinForm(forms.ModelForm):

    class Meta:
        model = PartnerJoin
        fields = (
            'full_name', 'email_address', 'company_or_business_name',
            'business_address_line_1', 'business_address_line_2', 'state_or_province',
            'country', 'zip_code', 'business_phone_number', 'website', 'product_type',
            'product_features_and_benefits', 'business_category',
        )
        widgets = {'country': CountrySelectWidget()}

    def clean_email_address(self, *args, **kwargs):
        email_address = self.cleaned_data.get('email_address')
        q_set = PartnerJoin.objects.filter(email_address__iexact=email_address)
        if q_set.exists():
            raise forms.ValidationError('This email already registered')
        return email_address


# Apply to sell on our platform
class SellApplyForm(forms.ModelForm):
    
    class Meta:
        model = SellApply
        fields = (
            'full_name', 'email', 'phone_number', 'country_of_citizenship', 'country_of_residence',
            'product_name', 'manufacturer', 'product_origin', 'product_description', 
            'date_produced', 'expiry_date', 'selling_price',
        )
        widgets = {'country': CountrySelectWidget()}