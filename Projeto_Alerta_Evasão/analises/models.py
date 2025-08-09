from django.db import models
from estudantes.models import Estudante

class PredicaoEvasao(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='predicoes')
    probabilidade = models.FloatField()
    previsao = models.CharField(max_length=20)
    nivel_risco = models.CharField(max_length=10, choices=[
        ('Baixo', 'Baixo'),
        ('Médio', 'Médio'),
        ('Alto', 'Alto'),
    ])
    data_predicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Predição de Evasão"
        verbose_name_plural = "Predições de Evasão"
        ordering = ['-data_predicao']
    
    def __str__(self):
        return f"Predição {self.estudante} - {self.nivel_risco}"