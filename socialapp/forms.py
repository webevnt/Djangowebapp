from django import forms
from socialapp.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password','email')


class UserProfileInfoForm(forms.ModelForm):
     class Meta:
         model = UserProfile
         fields = ('portfolio_site','description','city','profile_pic')
