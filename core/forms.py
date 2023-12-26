from django.forms import ModelForm
from .models import Casa




class CasaForm(ModelForm):
    class Meta:
        model = Casa
        fields = '__all__'


