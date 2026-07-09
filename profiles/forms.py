from django import forms
from .models import UserProfile

class UserProfileForm(forms.modelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        # database fields appear in the form
        fields = ['full_name', 
                  'email', 
                  'delivery_address', 
                  'delivery_notes']
        
        # text shown above the input
        labels = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'delivery_address': 'Delivery Address',
                'delivery_notes': 'Delivery Notes'
                }

        # controls the HTML input element used for each field
        widgets = {'full_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    'delivery_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
                   }

    def __init__ (self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(). __init__(*args, **kwargs)

        if self.user:
            self.fields['email'].initial = self.user.email

    def save(self,commit=True):
        profile = super().save(commit=True);

        if self.user:
            self.user.email = self.cleaned_data['email']

            if commit:
                self.user.save()
                profile.save()

        return profile