from django import forms
from sorl.thumbnail import ImageField
from taggit.forms import TagWidget, TagField

from .models import Article, Images, PointOfInterest


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Place Name',
                                      'class': 'uk-input'}),
        min_length=5,
        max_length=100,
        required=True)
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Description',
                                     'class': 'uk-input'}),
        max_length=3000,
        required=False)
    tags = TagField(
        required=False)

    class Meta:
        model = Article
        fields = ('title', 'text', 'tags')
        widgets = {'tags': TagWidget()}


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Images
        fields = ['image']


class Zone(forms.ModelForm):
    class Meta:
        model = PointOfInterest
        fields = ['position']
