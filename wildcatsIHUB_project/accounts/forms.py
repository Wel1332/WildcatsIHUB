from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re

class StudentLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@cit.edu'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '••••••••'
        })
    )

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.edu$', email):
            raise forms.ValidationError("Please enter a valid university email address (.edu domain).")
        return email