from .models import Estudante
from rest_framework import viewsets
from .serializers import EstudanteSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        summary='Listar todos os estudantes',
        description='''
        Retorna uma lista paginada de todos os estudantes cadastrados no sistema.
        
        Este endpoint permite visualizar todos os estudantes com suas informações
        acadêmicas completas, incluindo dados pessoais e desempenho acadêmico.
        ''',
        responses={
            200: EstudanteSerializer(many=True),
            401: 'Não autorizado',
            403: 'Acesso negado'
        },
        tags=['Estudantes'],
        examples=[
            OpenApiExample(
                'Lista de estudantes',
                value=[
                    {
                        'id': 1,
                        'nome': 'João Silva',
                        'matricula': '2024001',
                        'idade_ingresso': 18,
                        'genero': 1,
                        'turno_aulas': 1,
                        'bolsista': True,
                        'necessidades_especiais': False,
                        'disciplinas_aprovadas_1per': 8,
                        'disciplinas_matriculadas_1per': 10,
                        'nota_media_1per': 7.5
                    }
                ]
            )
        ]
    ),
    create=extend_schema(
        summary='Criar novo estudante',
        description='''
        Cadastra um novo estudante no sistema com todas as informações acadêmicas necessárias.
        
        **Campos obrigatórios:**
        - Nome completo
        - Matrícula (deve ser única)
        - Idade de ingresso
        - Gênero, turno e informações acadêmicas dos primeiros semestres
        ''',
        request=EstudanteSerializer,
        responses={
            201: EstudanteSerializer,
            400: 'Dados inválidos ou matrícula já existe',
            401: 'Não autorizado'
        },
        tags=['Estudantes'],
        examples=[
            OpenApiExample(
                'Dados para criação',
                value={
                    'nome': 'Maria Santos',
                    'matricula': '2024002',
                    'idade_ingresso': 19,
                    'genero': 0,
                    'turno_aulas': 0,
                    'bolsista': False,
                    'necessidades_especiais': False,
                    'disciplinas_aprovadas_1per': 7,
                    'disciplinas_matriculadas_1per': 9,
                    'nota_media_1per': 8.2,
                    'disciplinas_aprovadas_2per': 8,
                    'disciplinas_matriculadas_2per': 10,
                    'nota_media_2per': 7.8
                }
            )
        ]
    ),
    retrieve=extend_schema(
        summary='Buscar estudante por ID',
        description='''
        Retorna os dados completos de um estudante específico.
        
        Útil para visualizar detalhes individuais ou antes de realizar
        predições de evasão para o estudante.
        ''',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID único do estudante no sistema'
            )
        ],
        responses={
            200: EstudanteSerializer,
            404: 'Estudante não encontrado',
            401: 'Não autorizado'
        },
        tags=['Estudantes'],
        examples=[
            OpenApiExample(
                'Estudante encontrado',
                value={
                    'id': 1,
                    'nome': 'João Silva',
                    'matricula': '2024001',
                    'idade_ingresso': 18,
                    'genero': 1,
                    'turno_aulas': 1,
                    'bolsista': True,
                    'necessidades_especiais': False,
                    'disciplinas_aprovadas_1per': 8,
                    'disciplinas_matriculadas_1per': 10,
                    'nota_media_1per': 7.5,
                    'disciplinas_aprovadas_2per': 9,
                    'disciplinas_matriculadas_2per': 10,
                    'nota_media_2per': 8.0
                }
            )
        ]
    ),
    update=extend_schema(
        summary='Atualizar dados do estudante',
        description='''
        Atualiza completamente os dados de um estudante existente.
        
        **Atenção:** Esta operação substitui todos os dados do estudante.
        Para atualizações parciais, use o endpoint PATCH.
        ''',
        request=EstudanteSerializer,
        responses={
            200: EstudanteSerializer,
            400: 'Dados inválidos',
            404: 'Estudante não encontrado',
            401: 'Não autorizado'
        },
        tags=['Estudantes']
    ),
    partial_update=extend_schema(
        summary='Atualizar parcialmente o estudante',
        description='''
        Permite atualizar apenas campos específicos do estudante sem afetar os demais dados.
        
        Ideal para correções pontuais como atualização de notas ou
        informações acadêmicas de semestres específicos.
        ''',
        request=EstudanteSerializer,
        responses={
            200: EstudanteSerializer,
            400: 'Dados inválidos',
            404: 'Estudante não encontrado',
            401: 'Não autorizado'
        },
        tags=['Estudantes'],
        examples=[
            OpenApiExample(
                'Atualização de notas',
                value={
                    'nota_media_2per': 8.5,
                    'disciplinas_aprovadas_2per': 10
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary='Remover estudante',
        description='''
        Remove permanentemente um estudante do sistema.
        
        **Atenção:** Esta operação também removerá todas as predições 
        de evasão associadas ao estudante. Use com cautela.
        ''',
        responses={
            204: 'Estudante removido com sucesso',
            404: 'Estudante não encontrado',
            401: 'Não autorizado'
        },
        tags=['Estudantes']
    )
)
class EstudanteViewSet(viewsets.ModelViewSet): 
    """
    ViewSet completo para gerenciamento de estudantes.
    
    Fornece operações CRUD (Create, Read, Update, Delete) para o modelo Estudante,
    incluindo listagem, criação, busca individual, atualização e remoção.
    
    Os dados dos estudantes são utilizados pelo sistema de predição de evasão
    para realizar análises de Machine Learning.
    """
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
