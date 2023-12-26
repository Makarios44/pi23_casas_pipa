from django.db import models
# Create your models here.


class Casa(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_quartos = models.IntegerField()
    possui_piscina = models.BooleanField(default=False)
    introducao_casa = models.TextField()
    fotos = models.ImageField(upload_to='casas_fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome
    


   

