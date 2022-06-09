from django import forms
from .models import Post


class TagForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tag Name',
        }),
        required=False)
    weight = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Tag Weight',
        }),
        required=False)


class PostForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
        })
    )

    class Meta:
        model = Post
        fields = ['description']
