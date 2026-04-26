from django.shortcuts import render
from core.models import Pessoal
from .models import Certificado, Projeto

# Create your views here.

def home(request):
    pessoal = Pessoal.objects.first()
    certificados = Certificado.objects.all()

    context = {
        'pessoal': pessoal,
        'certificados': certificados
    }
    return render(request, 'portfolio/home.html', context)

def projetos(request):
    projetos_lista = Projeto.objects.all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos_lista})


def contato(request):
    return render(request, 'portfolio/contato.html')
