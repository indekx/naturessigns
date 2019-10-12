from django import forms


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