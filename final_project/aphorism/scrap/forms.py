from django import forms
from .models import Quotas, Tags, Authors


class SearchForm(forms.Form):
    quota = forms.CharField(label='Quote', required=False, widget=forms.TextInput(attrs={'class': 'formclass'}))
    author = forms.ModelChoiceField(queryset=Authors.objects.all(),  label='Author', required=False)
    tag = forms.ModelChoiceField(queryset=Tags.objects.all(),  label='Tags', required=False)

    class Meta:
        model = Quotas
        fields = ('quota', 'author', 'tag')
