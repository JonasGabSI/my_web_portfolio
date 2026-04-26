from django.db import models

class Pessoal(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    curso = models.CharField(max_length=100)
    periodo = models.CharField(max_length=20)
    email = models.EmailField()
    git = models.URLField(blank=True, null=True) 
    linked = models.URLField(blank=True, null=True)
    url_imagem = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome

# Create your models here.
