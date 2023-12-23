from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Casa(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_quartos = models.IntegerField()
    possui_piscina = models.BooleanField(default=False)
    introducao_casa = models.TextField()
    fotos = models.ImageField(upload_to='casas_fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # campo pra verificar se o usuário vai anunciar para locação ou vai alugar
    ANUNCIAR = 'anunciar'
    ALUGAR = 'alugar'
    OPCOES_TIPO = [
        (ANUNCIAR, 'Anunciar para locação'),
        (ALUGAR, 'Buscar para alugar'),
    ]
    tipo_usuario = models.CharField(max_length=10, choices=OPCOES_TIPO, default=ANUNCIAR)

    def __str__(self):
        return self.username


