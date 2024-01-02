from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.contrib.auth.models import User
# Create your models here.


class Casa(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_quartos = models.IntegerField()
    possui_piscina = models.BooleanField(default=False)
    introducao_casa = models.TextField()
    fotos = models.ImageField(upload_to='media', blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
       return f'{self.nome} {self.quantidade_quartos} {self.fotos} {self.possui_piscina} {self.introducao_casa} {self.preco}'
    

class Reserva(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    data_check_in = models.DateField()
    data_check_out = models.DateField()