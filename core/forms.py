from django.forms import ModelForm
from .models import Casa




class CasaForm(ModelForm):
    class Meta:
        model = Casa
        fields = ['nome','quantidade_quartos','possui_piscina','introducao_casa','preco','fotos']


