from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from system.models import OrderHere, FLAVOUR_CHOICES


class OrderHereForm(forms.ModelForm):
    class Meta:
        model = OrderHere
        fields = '__all__'


class ContactForm(forms.Form):
    # These fields correspond to {{ form.name }}, {{ form.email }}, etc. in your template

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            # The CSS in contact.html automatically styles input elements inside .form-group
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'john@example.com',
        })
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your event...',
            'rows': 4,
        })
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'  # Adds hook for CSS if needed
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))


# --- NEW: Register Form ---
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address'
    }))

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Add placeholders to generated fields
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a Username'

class OrderForm(forms.Form):
    flavour = forms.ChoiceField(
        choices=[('', 'Select a Flavour')] + FLAVOUR_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'flavour-select'})
    )
    weight = forms.DecimalField(
        required=True,
        min_value=1.0,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight in Kg (Min 1.0)', 'step': '0.5', 'id': 'id_weight'})
    )
    date_needed = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'placeholder': 'Date Required', 'type': 'date'})
    )
    cake_message = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Message on Cake (Optional)'})
    )
    details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Design preference, allergies, or special instructions...', 'rows': 4})
    )