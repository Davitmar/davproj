from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class UserRegForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={'class': 'formclass'}))
    first_name = forms.CharField(label='First Name', required=True,widget=forms.TextInput(attrs={'class': 'formclass'}))
    last_name = forms.CharField(label='Last Name',required=True, widget=forms.TextInput(attrs={'class': 'formclass'}))
    password1 = forms.CharField(label='Password', required=True,widget=forms.PasswordInput(attrs={'class': 'formclass'}))
    password2 = forms.CharField(label='Password', required=True,widget=forms.PasswordInput(attrs={'class': 'formclass'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'formclass'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'formclass'}))


