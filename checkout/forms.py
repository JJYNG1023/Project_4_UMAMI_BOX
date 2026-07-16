from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    street_address_1 = forms.CharField(max_length=80)
    street_address_2 = forms.CharField(max_length=80, required=False)
    postcode = forms.CharField(max_length=20)
    town_or_city = forms.CharField(max_length=80)
    country = CountryField(blank_label='Country').formfield(
        widget=CountrySelectWidget(attrs={'class': 'profile-form-input'})
    )
    delivery_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'profile-form-textarea',
            'rows': 4
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address_1': 'Street Address 1',
            'street_address_2': 'Street Address 2',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
        }

        for field_name, field in self.fields.items():
            if field_name != 'country':
                field.widget.attrs['class'] = 'profile-form-input'

            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]