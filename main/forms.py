from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    # We add these fields manually to make them required
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        # These are the fields that will show up on the HTML page
        fields = ('username', 'first_name', 'last_name', 'email')