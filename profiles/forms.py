from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'profile-form-input'})
)

    class Meta:
        model = UserProfile
        # database fields appear in the form
        fields = [            
                    'full_name',
                    'email',
                    'phone_number',
                    'street_address_1',
                    'street_address_2',
                    'postcode',
                    'town_or_city',
                    'country',
                    'delivery_notes',]
        
        # controls the HTML input element used for each field
        widgets = {
                    'full_name': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'email': forms.EmailInput(attrs={'class': 'profile-form-input'}),
                    'phone_number': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'street_address_1': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'street_address_2': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'postcode': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'town_or_city': forms.TextInput(attrs={'class': 'profile-form-input'}),
                    'country': forms.Select(attrs={'class': 'profile-form-input'}),
                    'delivery_notes': forms.Textarea(attrs={
                        'class': 'profile-form-textarea',
                        'rows': 5,
                    }),
                }

    def __init__ (self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(). __init__(*args, **kwargs)

        if self.user:
            self.fields['email'].initial = self.user.email

    def save(self,commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.email = self.cleaned_data['email']

        if commit:
            if self.user:
                self.user.save()

            profile.save()

        return profile