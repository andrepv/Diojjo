from django import forms
from django.forms import ModelForm
from authentication.models import Profile
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'uk-input'}),
        min_length=5,
        max_length=25,
        required=True)
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Location',
            'class': 'uk-input'}),
        max_length=25,
        required=False)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'About you',
            'class': 'uk-input',
        }),
        max_length=100,
        required=False
        )

    class Meta:
        model = User
        fields = ['username', 'location', 'bio']


class PhotoForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
