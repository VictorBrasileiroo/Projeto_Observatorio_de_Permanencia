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

class PredicaoInputSerializer(serializers.Serializer):
    matricula = serializers.CharField(max_length=9)
    idade_ingresso = serializers.IntegerField(min_value=15, max_value=70)
    genero = serializers.ChoiceField(choices=[(0, 'Feminino'), (1, 'Masculino')])  
    turno_aulas = serializers.ChoiceField(choices=[(0, 'Noturno'), (1, 'Diurno')])        
    bolsista = serializers.BooleanField(default=False)
    necessidades_especiais = serializers.BooleanField(default=False)
    disciplinas_aprovadas_1per = serializers.IntegerField(min_value=0)
    disciplinas_matriculadas_1per = serializers.IntegerField(min_value=0)
    nota_media_1per = serializers.FloatField(min_value=0, max_value=20)
    disciplinas_aprovadas_2per = serializers.IntegerField(min_value=0)
    disciplinas_matriculadas_2per = serializers.IntegerField(min_value=0)
    nota_media_2per = serializers.FloatField(min_value=0, max_value=20)
