from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import timedelta
from django.utils import timezone
from django.db.models import ExpressionWrapper, F, BooleanField
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
    
    def marcar_datas_reservadas(self, data_check_in, data_check_out):
        datas_reserva = [data_check_in + timezone.timedelta(days=x) for x in range((data_check_out - data_check_in).days + 1)]

        # Adicione o relacionamento reverso 'reservas'
        for data_reserva in datas_reserva:
            Reserva.objects.create(casa=self, data_reserva=data_reserva)

    def is_casa_disponivel(self, check_in_date, check_out_date):
        reservas = Reserva.objects.filter(casa=self, data_check_out__gte=check_in_date, data_check_in__lte=check_out_date)
        return not reservas.exists()

    
    
class Reserva(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    data_check_in = models.DateField()
    data_check_out = models.DateField()
    data_reserva = models.DateTimeField(default=timezone.now)