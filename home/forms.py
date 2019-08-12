from .models import Post,Comment
from django import forms

class HomeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)