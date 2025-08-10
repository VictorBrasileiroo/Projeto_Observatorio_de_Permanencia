from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from estudantes.models import Estudante
from analises.models import PredicaoEvasao
from .serializers import PredicaoEvasaoSerializer
from .services import modelo_service
from django.db.models import Avg

@extend_schema(
    summary='Analisar evasão para todos os estudantes',
    description='''
    Executa predições de evasão para todos os estudantes cadastrados no sistema.
    
    Este endpoint aplica o modelo de Machine Learning em todos os estudantes que ainda não possuem 
    predições cadastradas, gerando análises de risco de evasão baseadas em dados acadêmicos.
    
    **Processo:**
    1. Busca todos os estudantes cadastrados
    2. Filtra apenas estudantes sem predições existentes
    3. Aplica o modelo ML para cada estudante
    4. Salva as predições no banco de dados
    5. Retorna relatório detalhado do processamento
    ''',
    request=None,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'mensagem': {
                    'type': 'string',
                    'description': 'Resumo do processamento'
                },
                'total_alunos_analisados': {
                    'type': 'integer',
                    'description': 'Total de estudantes no sistema'
                },
                'predicoes_criadas': {
                    'type': 'integer',
                    'description': 'Número de novas predições geradas'
                },
                'predicoes_com_erro': {
                    'type': 'integer',
                    'description': 'Número de predições que falharam'
                },
                'detalhes_predicoes': {
                    'type': 'array',
                    'description': 'Lista detalhada das predições criadas',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'estudante_id': {'type': 'integer'},
                            'matricula_estudante': {'type': 'string'},
                            'previsao': {'type': 'string', 'enum': ['Evasão', 'Não evasão']},
                            'nivel_risco': {'type': 'string', 'enum': ['Alto', 'Médio', 'Baixo']},
                            'probabilidade': {'type': 'string', 'description': 'Probabilidade formatada em percentual'}
                        }
                    }
                },
                'erros': {
                    'type': 'array',
                    'description': 'Lista de erros ocorridos durante o processamento',
                    'nullable': True
                }
            }
        },
        400: 'Nenhum estudante cadastrado no sistema',
        500: 'Erro interno do servidor ou do modelo ML'
    },
    tags=['Análises de Evasão'],
    examples=[
        OpenApiExample(
            'Processamento bem-sucedido',
            value={
                'mensagem': '5 predições criadas',
                'total_alunos_analisados': 10,
                'predicoes_criadas': 5,
                'predicoes_com_erro': 0,
                'detalhes_predicoes': [
                    {
                        'estudante_id': 1,
                        'matricula_estudante': '2024001',
                        'previsao': 'Evasão',
                        'nivel_risco': 'Alto',
                        'probabilidade': '85.50%'
                    }
                ],
                'erros': None
            }
        ),
        OpenApiExample(
            'Nenhuma predição necessária',
            value={
                'mensagem': 'Nenhuma predição foi realizada, pois todos os alunos já possuem predições cadastradas ou não há alunos disponíveis'
            }
        )
    ]
)
@api_view(['POST'])
def analise_evasao_todos_estudantes(request):
    estudantes = Estudante.objects.all()

    if not estudantes.exists():
        return Response({
            'erro' : 'Nenhum estudante cadastrado'
        }, status=400)
    
    predicoes_criadas = []
    predicoes_com_erro = []
    
    for estudante in estudantes:
        if PredicaoEvasao.objects.filter(estudante=estudante).exists():
            continue
        
        try:
            resultado = modelo_service.prever_evasao_estudante(estudante)

            predicao = PredicaoEvasao.objects.create(
                estudante = estudante,
                probabilidade = resultado['probabilidade'],
                previsao = resultado['previsao'],
                nivel_risco = resultado['nivel_risco']
            )

            predicoes_criadas.append({
                'estudante_id': estudante.id,
                'matricula_estudante': estudante.matricula,
                'previsao': resultado['previsao'],
                'nivel_risco': resultado['nivel_risco'],
                'probabilidade': f"{resultado['probabilidade']:.2%}"
            })

        except Exception as ex:
            predicoes_com_erro.append({
                'estudante_id': estudante.id,
                'erro' : str(ex) 
            })
            continue

    if len(predicoes_criadas) == 0:
        return Response({
            'mensagem': 'Nenhuma predição foi realizada, pois todos os alunos já possuem predições cadastradas ou não há alunos disponíveis'
        })
    else:
        return Response({
            'mensagem': f'{len(predicoes_criadas)} predições criadas',
            'total_alunos_analisados': estudantes.count(),
            'predicoes_criadas': len(predicoes_criadas),
            'predicoes_com_erro': len(predicoes_com_erro),
            'detalhes_predicoes': predicoes_criadas,
            'erros': predicoes_com_erro if predicoes_com_erro else None
        })

@extend_schema(
    summary='Listar todas as predições de evasão',
    description='''
    Retorna uma lista completa de todas as predições de evasão realizadas, 
    ordenadas por data de criação (mais recentes primeiro).
    
    Cada predição inclui informações do estudante, resultado da análise ML,
    probabilidade calculada e nível de risco atribuído.
    ''',
    responses={
        200: PredicaoEvasaoSerializer(many=True),
        404: 'Nenhuma predição encontrada'
    },
    tags=['Análises de Evasão'],
    examples=[
        OpenApiExample(
            'Lista de predições',
            value=[
                {
                    'id': 1,
                    'estudante': {
                        'id': 1,
                        'nome': 'João Silva',
                        'matricula': '2024001'
                    },
                    'probabilidade': 0.85,
                    'previsao': 'Evasão',
                    'nivel_risco': 'Alto',
                    'data_predicao': '2025-08-10T14:30:00Z'
                }
            ]
        )
    ]
)
@api_view(['GET'])
def listar_predicoes(request):
    predicoes = PredicaoEvasao.objects.all().order_by('-data_predicao')
       
    serializer = PredicaoEvasaoSerializer(predicoes, many=True)
    
    return Response(serializer.data)


@extend_schema(
    summary='Limpar todas as predições',
    description='''
    Remove todas as predições de evasão do sistema, mantendo os dados dos estudantes intactos.
    
    **Atenção:** Esta operação é irreversível e removerá permanentemente todas as 
    análises de evasão realizadas. Use com cautela em ambiente de produção.
    ''',
    request=None,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'mensagem': {
                    'type': 'string',
                    'description': 'Confirmação da remoção com quantidade removida'
                },
                'alunos_mantidos': {
                    'type': 'integer',
                    'description': 'Número total de estudantes que permaneceram no sistema'
                }
            }
        }
    },
    tags=['Análises de Evasão'],
    examples=[
        OpenApiExample(
            'Limpeza realizada',
            value={
                'mensagem': '150 predições removidas',
                'alunos_mantidos': 200
            }
        )
    ]
)
@api_view(['DELETE'])
def limpar_predicoes(request):
    
    total_removidas = PredicaoEvasao.objects.count()
    PredicaoEvasao.objects.all().delete()
    
    return Response({
        'mensagem': f'{total_removidas} predições removidas',
        'alunos_mantidos': Estudante.objects.count()
    })

@extend_schema(
    summary='Gerar relatório completo das análises',
    description='''
    Gera um relatório estatístico abrangente sobre todas as predições de evasão realizadas no sistema.
    
    **O relatório inclui:**
    - Resumo geral com cobertura de análises
    - Distribuição por níveis de risco (Alto/Médio/Baixo)
    - Estatísticas de previsões (Evasão/Não evasão)
    - Métricas como probabilidade média de evasão
    
    Ideal para análises gerenciais e tomada de decisões institucionais.
    ''',
    request=None,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'mensagem': {
                    'type': 'string',
                    'description': 'Status da geração do relatório'
                },
                'resumo_geral': {
                    'type': 'object',
                    'properties': {
                        'total_alunos_cadastrados': {'type': 'integer'},
                        'total_analises_realizadas': {'type': 'integer'},
                        'alunos_sem_predicao': {'type': 'integer'},
                        'cobertura_de_analises': {'type': 'string', 'description': 'Percentual de cobertura'}
                    }
                },
                'distribuicao_risco': {
                    'type': 'object',
                    'properties': {
                        'alto_risco': {'type': 'integer'},
                        'medio_risco': {'type': 'integer'},
                        'baixo_risco': {'type': 'integer'}
                    }
                },
                'previsoes': {
                    'type': 'object',
                    'properties': {
                        'evasao_prevista': {'type': 'integer'},
                        'nao_evasao_prevista': {'type': 'integer'},
                        'taxa_evasao_prevista': {'type': 'string', 'description': 'Percentual de evasão prevista'}
                    }
                },
                'metricas': {
                    'type': 'object',
                    'properties': {
                        'probabilidade_media_evasao': {'type': 'string', 'description': 'Probabilidade média com 3 casas decimais'}
                    }
                }
            }
        }
    },
    tags=['Relatórios'],
    examples=[
        OpenApiExample(
            'Relatório completo',
            value={
                'mensagem': 'relatório criado com sucesso',
                'resumo_geral': {
                    'total_alunos_cadastrados': 200,
                    'total_analises_realizadas': 180,
                    'alunos_sem_predicao': 20,
                    'cobertura_de_analises': '90.0%'
                },
                'distribuicao_risco': {
                    'alto_risco': 45,
                    'medio_risco': 90,
                    'baixo_risco': 45
                },
                'previsoes': {
                    'evasao_prevista': 50,
                    'nao_evasao_prevista': 130,
                    'taxa_evasao_prevista': '27.8%'
                },
                'metricas': {
                    'probabilidade_media_evasao': '0.342'
                }
            }
        )
    ]
)
@api_view(['GET'])
def gerar_relatorio_das_analises(request):
    total_alunos = Estudante.objects.count()
    total_predicoes = PredicaoEvasao.objects.count()

    risco_alto = PredicaoEvasao.objects.filter(nivel_risco='Alto').count()
    risco_medio = PredicaoEvasao.objects.filter(nivel_risco='Médio').count()
    risco_baixo = PredicaoEvasao.objects.filter(nivel_risco='Baixo').count()

    previsao_evasao = PredicaoEvasao.objects.filter(previsao='Evasão').count()
    previsao_nao_evasao = PredicaoEvasao.objects.filter(previsao='Não evasão').count()

    alunos_analisados = PredicaoEvasao.objects.values('estudante').distinct().count()
    alunos_nao_analisados = total_alunos - alunos_analisados

    probabilidade_media_evasao = PredicaoEvasao.objects.aggregate(Avg('probabilidade'))['probabilidade__avg']

    return Response({
        'mensagem': 'relatório criado com sucesso',
        'resumo_geral': {
            'total_alunos_cadastrados': total_alunos,
            'total_analises_realizadas': total_predicoes,
            'alunos_sem_predicao': alunos_nao_analisados,
            'cobertura_de_analises': f"{(alunos_analisados/total_alunos*100):.1f}%" if total_alunos > 0 else "0%"
        },
        'distribuicao_risco': {
            'alto_risco': risco_alto,
            'medio_risco': risco_medio,
            'baixo_risco': risco_baixo
        },
        'previsoes': {
            'evasao_prevista': previsao_evasao,
            'nao_evasao_prevista': previsao_nao_evasao,
            'taxa_evasao_prevista': f"{(previsao_evasao/total_predicoes*100):.1f}%" if total_predicoes > 0 else "0%"
        },
        'metricas': {
            'probabilidade_media_evasao': f"{probabilidade_media_evasao:.3f}" if probabilidade_media_evasao else "N/A"
        }
    })


