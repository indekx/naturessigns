from django import forms
from business import models
from django.contrib.auth.models import User


GENDER = (
    ('', 'select'),
    ('FE', 'Female'),
    ('MA', 'Male')
)

STATES = (
    ('', 'Choose'),
    ('AB', 'Abia'),
    ('AD', 'Adamawa'),
    ('AK', 'Akwa Ibom'),
    ('AN', 'Anambra'),
    ('BA', 'Bauchi'),
    ('BY', 'Bayelsa'),
    ('BE', 'Benue'),
    ('BO', 'Bornu'),
    ('CR', 'Cross River'),
    ('DE', 'Delta'),
    ('EB', 'Ebonyi'),
    ('ED', 'Edo'),
    ('EK', 'Ekiti'),
    ('EN', 'Enugu'),
    ('FC', 'Federal Capital Territory'),
    ('GO', 'Gombe'),
    ('IM', 'Imo'),
    ('JI', 'Jigawa'),
    ('KD', 'Kaduna'),
    ('KN', 'Kano'),
    ('KT', 'Katsina'),
    ('KE', 'Kebbi'),
    ('KO', 'Kogi'),
    ('KW', 'Kwara'),
    ('LA', 'Lagos'),
    ('NA', 'Nasarawa'),
    ('NI', 'Niger'),
    ('OG', 'Ogun'),
    ('ON', 'Ondo'),
    ('OS', 'Osun'),
    ('OY', 'Oyo'),
    ('PL', 'Plateau'),
    ('RI', 'Rivers'),
    ('SO', 'Sokoto'),
    ('TA', 'Taraba'),
    ('YO', 'Yobe'),
    ('ZA', 'Zamfara')
)


class BecomeAnAffiliate(forms.ModelForm):
    class Meta:
        model = models.BecomeAnAffiliate
        fields = [
            'first_name',
            'last_name',
            'email',
            'job_title',
            'contact_phone_number',
            'tell_us_about_you',
            'company_name',
            'contact_address',
            'city',
            'state',
            'country',
            'website',

         ]
        
    login_url = '/login/'


# Distribution Application
class DistributorApplication(forms.Form):

    # Personal Data
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}), label="", max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}), label="", max_length=100, required=True)
    gender = forms.ChoiceField(choices=GENDER, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your email'}), label="", max_length=254, required=True)
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Address Line 1'}), label="", min_length=4, max_length=500, required=True)
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Address Line 2'}), label="", min_length=4, max_length=500, required=False)
    city = forms.CharField()
    phone_number = forms.CharField()
    state = forms.ChoiceField(choices=STATES, required=True)
    age = forms.IntegerField(min_value=16)

    # Referee's Data

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}), label="", max_length=100, required=True)
    contact_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Contact address'}), label="", min_length=4, max_length=500, required=True)
    occupation = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Occupation'}), label="", min_length=4, max_length=500, required=True)
    mobile_number = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'gender',
            'age',
            'email',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'phone_number',
            'full_name',
            'ontact_address',
            'occupation ',
            'mobile_number',
         ]
    
    login_url = '/login/'


