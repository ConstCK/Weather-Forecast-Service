from django import forms

from forecast.models import ForecastRequest


class ForecastRequestForm(forms.ModelForm):
    class Meta:
        model = ForecastRequest
        fields = ['city']
        widgets = {
            'city': forms.TextInput(
                attrs={
                    'list': 'city-options',
                    'id': 'id_city',
                    'class': 'city-input'
                }
            )
        }
