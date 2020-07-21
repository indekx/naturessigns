from django import forms
from phonenumber_field.formfields import PhoneNumberField

STATES = (
    ('', 'select'),
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
    ('FCT', 'Federal Capital Territory'),
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


class CheckOutForm(forms.Form):
    shipping_address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Shipping Address Line 1'}), label="", max_length=254, required=True)
    shipping_address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Shipping Address Line 2'}), label="", max_length=254, required=False)
    state = forms.ChoiceField(choices=STATES, label='')
    phone_number = forms.CharField(required=True)
    zip_code = forms.CharField(required=False, max_length=6)
    same_as_shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())


""" class AddProduct(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
            'title',
            'category',
            'image',
            'description',
         ]
        
    login_url = '/login/'  """

class ContactUsForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}
        ), label="", max_length=65, required=True
    )
    
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}
        ), label="", max_length=65, required=True
    )
    
    contact_email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email Address'}
        ), label="", max_length=254, required=True
    )

    contact_phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone ( Optional )' }
        ), label="", max_length=15, required=False
    )

    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Leave Us Your Message'}
        ), label="", max_length=1500, required=True 
    )