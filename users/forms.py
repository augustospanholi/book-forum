from django import forms


class LoginForms(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Your username'}),
    )
    password = forms.CharField(
        label='Password',
        required=True,
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'field-input', 'placeholder': 'Your password'}),
    )


class RegistrationForms(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'field-input', 'placeholder': 'Choose a username'}),
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'field-input', 'placeholder': 'your@email.com'}),
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'field-input', 'placeholder': 'Create a password'}),
    )
    password2 = forms.CharField(
        label='Confirm your password',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'field-input', 'placeholder': 'Repeat your password'}),
    )
