from rest_framework import serializers
from estudantes.models import Estudante
from .models import PredicaoEvasao

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = '__all__'

class EstudanteResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id', 'matricula', 'idade_ingresso', 'genero', 'turno_aulas']

class PredicaoEvasaoSerializer(serializers.ModelSerializer):
    estudante_dados = EstudanteResumoSerializer(source='estudante', read_only=True) 

    class Meta:
        model = PredicaoEvasao
        fields = ['id', 'probabilidade', 'previsao', 'nivel_risco', 'data_predicao', 'estudante', 'estudante_dados']
