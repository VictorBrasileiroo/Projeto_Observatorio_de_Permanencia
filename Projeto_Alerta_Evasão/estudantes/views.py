from .models import Estudante
from rest_framework import viewsets
from .serializers import EstudanteSerializer

class EstudanteViewSet(viewsets.ModelViewSet): 
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
