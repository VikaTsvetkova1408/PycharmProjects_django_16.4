from django import forms
from .models import Author, Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content'
        ]


