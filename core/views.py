from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Pessoal
from .serializers import PessoalSerializer

def home(request):
    return render(request, 'portfolio/home.html')

class PerfilDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PessoalSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        perfil, created = Pessoal.objects.get_or_create(
            usuario=self.request.user,
            defaults={'nome': self.request.user.username},
        )
        return perfil

# Create your views here.
