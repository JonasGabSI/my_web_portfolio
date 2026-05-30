from django.db import models
from django.conf import settings

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tarefas',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.titulo
    
# Create your models here.
