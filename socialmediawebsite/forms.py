from django import forms

from .models import Post


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
