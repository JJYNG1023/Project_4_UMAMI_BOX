from django import forms
from .models import Product

SPICE_LEVEL_CHOICES = [
    ('', 'Select spice level'),
    ('Mild', 'Mild'),
    ('Medium', 'Medium'),
    ('Hot', 'Hot'),
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            'cooking_time': 'Cooking time in Min',
            'spice_level': 'Spice level',
            }

        widgets = {
            'spice_level': forms.Select(choices=SPICE_LEVEL_CHOICES),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'