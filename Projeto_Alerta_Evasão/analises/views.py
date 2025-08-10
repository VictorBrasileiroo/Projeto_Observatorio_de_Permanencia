from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from estudantes.models import Estudante
from analises.models import PredicaoEvasao
from .serializers import PredicaoEvasaoSerializer
from .services import modelo_service
from django.db.models import Avg

@extend_schema(responses={200: dict})
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

@extend_schema(responses={200: PredicaoEvasaoSerializer(many=True)})
@api_view(['GET'])
def listar_predicoes(request):
    predicoes = PredicaoEvasao.objects.all().order_by('-data_predicao')
       
    serializer = PredicaoEvasaoSerializer(predicoes, many=True)
    
    return Response(serializer.data)


@extend_schema(responses={200: dict})
@api_view(['DELETE'])
def limpar_predicoes(request):
    
    total_removidas = PredicaoEvasao.objects.count()
    PredicaoEvasao.objects.all().delete()
    
    return Response({
        'mensagem': f'{total_removidas} predições removidas',
        'alunos_mantidos': Estudante.objects.count()
    })

@extend_schema(responses={200:dict})
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


