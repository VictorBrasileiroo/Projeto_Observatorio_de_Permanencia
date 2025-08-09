from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from estudantes.models import Estudante
from analises.models import PredicaoEvasao
from .serializers import PredicaoEvasaoSerializer
from .services import modelo_service

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