from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Estudante

class EstudanteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.estudante_exemplo = Estudante.objects.create(
            matricula='202301001',
            idade_ingresso=18,
            genero=1,  
            turno_aulas=1, 
            bolsista=True,
            necessidades_especiais=False,
            disciplinas_aprovadas_1per=5,
            disciplinas_matriculadas_1per=6,
            nota_media_1per=8.5,
            disciplinas_aprovadas_2per=4,
            disciplinas_matriculadas_2per=5,
            nota_media_2per=7.8
        )

    def test_criacao_estudante_sucesso(self):
        estudante = Estudante.objects.create(
            matricula='202301002',
            idade_ingresso=28,
            genero=0,  
            turno_aulas=1, 
            bolsista=True,
            necessidades_especiais=False,
            disciplinas_aprovadas_1per=2,
            disciplinas_matriculadas_1per=6,
            nota_media_1per=3.5,
            disciplinas_aprovadas_2per=3,
            disciplinas_matriculadas_2per=5,
            nota_media_2per=4.8 
        )   

        self.assertEqual(estudante.matricula, '202301002')
        self.assertEqual(estudante.idade_ingresso, 28)
        self.assertEqual(estudante.genero, 0)
        self.assertTrue(estudante.bolsista)
        self.assertTrue(Estudante.objects.filter(matricula='202301002').exists())

    def test_matricula_unica(self):
        with self.assertRaises(IntegrityError):
            Estudante.objects.create(
                matricula='202301001',
                idade_ingresso=28,
                genero=0,  
                turno_aulas=1, 
                bolsista=True,
                necessidades_especiais=False,
                disciplinas_aprovadas_1per=2,
                disciplinas_matriculadas_1per=6,
                nota_media_1per=3.5,
                disciplinas_aprovadas_2per=3,
                disciplinas_matriculadas_2per=5,
                nota_media_2per=4.8    
            )

    def test_valor_invalido(self):
        estudante = Estudante(
            matricula='202301004',
            genero=5,  
            idade_ingresso=18,
            turno_aulas=1,
            disciplinas_aprovadas_1per=5,
            disciplinas_matriculadas_1per=6,
            nota_media_1per=8.0,
            disciplinas_aprovadas_2per=4,
            disciplinas_matriculadas_2per=5,
            nota_media_2per=7.5
        )

        with self.assertRaises(ValidationError):
            estudante.full_clean()

