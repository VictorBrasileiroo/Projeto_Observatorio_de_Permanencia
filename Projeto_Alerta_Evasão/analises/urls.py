from django.urls import path
from . import views

urlpatterns = [
    path('analisar_todos_estudantes/', views.analise_evasao_todos_estudantes, name='analisar_todos'),
    path('remover_todas_analises/', views.limpar_predicoes, name='remover_todas_analises'),
    path('listar_todas_analises/', views.listar_predicoes, name='listar_todas_analises'),
]