from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def EmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('Email already exists.')


def UsernameValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('Username already exists.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username',
                                      'class': 'uk-input'}),
        min_length=5,
        max_length=25,
        required=True)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                       'class': 'uk-input'}),
        max_length=60,
        required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': 'uk-input'}),
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': 'uk-input'}),
        required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')
        self.fields['username'].validators.append(UsernameValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['email'].validators.append(EmailValidator)
