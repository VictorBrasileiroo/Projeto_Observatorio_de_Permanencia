from django.db import models

class Estudante(models.Model):
    matricula = models.CharField(max_length=9, unique=True, verbose_name="Matrícula")
    idade_ingresso = models.IntegerField(verbose_name="Idade de Ingresso")
    genero = models.IntegerField(choices=[(0, 'Feminino'), (1, 'Masculino')], verbose_name="Gênero")
    turno_aulas = models.IntegerField(choices=[(0, 'Noturno'), (1, 'Diurno')], verbose_name="Turno das Aulas")
    bolsista = models.BooleanField(default=False, verbose_name="Bolsista")
    necessidades_especiais = models.BooleanField(default=False, verbose_name="Necessidades Especiais")
    disciplinas_aprovadas_1per = models.IntegerField(verbose_name="Disciplinas Aprovadas 1º Período")
    disciplinas_matriculadas_1per = models.IntegerField(verbose_name="Disciplinas Matriculadas 1º Período")
    nota_media_1per = models.FloatField(verbose_name="Nota Média 1º per")
    disciplinas_aprovadas_2per = models.IntegerField(verbose_name="Disciplinas Aprovadas 2º Período")
    disciplinas_matriculadas_2per = models.IntegerField(verbose_name="Disciplinas Matriculadas 2º Período")
    nota_media_2per = models.FloatField(verbose_name="Nota Média 2º Período")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Estudante {self.id}"