from django import forms
from scraping.models import City, Specialization


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label = 'Город'
    )
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label = 'Специальность'
    )
