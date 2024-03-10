from django import forms

from .models import Card


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ('date', )
        widgets = {
            'date': forms.DateInput(attrs={'required': True, 'type': 'date'}),
        }
        labels = {
            'date': '',
        }