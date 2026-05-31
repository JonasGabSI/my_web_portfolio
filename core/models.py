from django.db import models
from django.conf import settings

class Pessoal(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
        null=True,
        blank=True,
    )

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    curso = models.CharField(max_length=100)
    periodo = models.CharField(max_length=20)
    email = models.EmailField()
    git = models.URLField(blank=True) 
    linked = models.URLField(blank=True)
    url_imagem = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Perfil Pessoal'
        verbose_name_plural = 'Perfis Pessoais'

    def __str__(self):
        return self.nome

# Create your models here.
