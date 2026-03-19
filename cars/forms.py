from django import forms
from cars.models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'brand', 'factory_year', 'model_year', 'plate', 'value', 'photo','bio']

        
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value < 20000:
            self.add_error('value', "Valor minimo do carro deve ser R$20.000")
        return value
    
