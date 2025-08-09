from rest_framework import serializers
from .models import Estudante

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = '__all__'

        def validar_Matricula(self, value):
            if Estudante.objects.filter(matricula=value).exists(): raise serializers.ValidationError("Matrícula já cadastrada")
            return value