from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = [
            'full_name',
            'email',
            'phone_number',
            'street_address_1',
            'street_address_2',
            'postcode',
            'town_or_city',
            'country',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Email Address',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Phone Number',
            }),
            'street_address_1': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Street Address 1',
            }),
            'street_address_2': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Street Address 2',
            }),
            'postcode': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Postcode',
            }),
            'town_or_city': forms.TextInput(attrs={
                'class': 'profile-form-input',
                'placeholder': 'Town or City',
            }),
            'country': CountrySelectWidget(attrs={
                'class': 'profile-form-input',
            }),
        }


class DeliveryDateForm(forms.ModelForm):
    class Meta:
        model= Order
        fields = [
            'delivery_date',
            'delivery_time',
            'delivery_notes',
        ]

        widgets = {
            'delivery_date': forms.TextInput(attrs={
                'class': 'profile-form-input delivery-date-picker',
                'id': 'deliveryDatePicker',
                'placeholder': 'Choose delivery date',
            }),
            'delivery_time': forms.TimeInput(attrs={
                'class': 'profile-form-input',
                'type': 'time',
            }),
            'delivery_notes': forms.Textarea(attrs={
                'class': 'profile-form-textarea',
                'rows': 4,
                'placeholder': 'Add delivery notes...',
            }),
        }