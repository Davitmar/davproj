from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Quotas, Tags, Authors, Messege
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    quota = forms.CharField(label='Quote', required=False, widget=forms.TextInput(attrs={'class': 'formclass'}))
    author = forms.ModelChoiceField(queryset=Authors.objects.all(),  label='Author', required=False)
    tag = forms.ModelChoiceField(queryset=Tags.objects.all(),  label='Tags', required=False)

    class Meta:
        model = Quotas
        fields = ('quota', 'author', 'tag')

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Find users', required=False, widget=forms.TextInput(attrs={'placeholder':'username, name, last_name'}))


    class Meta:
        model = User
        fields = ('username', )

class MessegeSearchForm(forms.Form):
    sender = forms.CharField(label='Search', required=False, widget=forms.TextInput(attrs={'class': 'formclass'}))

    class Meta:
        model = Messege
        fields = ('sender',)

