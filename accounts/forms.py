from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'class': 'smalltextfield'}),
        label="Username",
        help_text="Enter your username"
    )
    email = forms.EmailField(
        help_text="Enter your email address",
        widget=forms.EmailInput(attrs={'class': 'smalltextfield'}),
        label="Email Address")
    password1 = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'class': 'smalltextfield'}),
        label="Password",
        help_text="Enter a password"
    )
    password2 = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'class': 'smalltextfield'}),
        label="Confirm Password",
        label_suffix=":",
        help_text="Re-enter your password"
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
