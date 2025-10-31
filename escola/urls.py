# urls.py
from django.urls import path
from . import views

app_name = 'escola'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Turmas
    path('turmas/', views.lista_turmas, name='lista_turmas'),
    path('turmas/criar/', views.criar_turma, name='criar_turma'),
    path('turmas/<int:pk>/', views.detalhes_turma, name='detalhes_turma'),
    path('turmas/<int:pk>/editar/', views.editar_turma, name='editar_turma'),
    
    # Alunos
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    path('alunos/<int:pk>/', views.detalhes_aluno, name='detalhes_aluno'),
    
    # Materiais
    path('turmas/<int:turma_id>/materiais/criar/', views.criar_material, name='criar_material'),
    path('materiais/<int:pk>/editar/', views.editar_material, name='editar_material'),
    path('materiais/<int:pk>/deletar/', views.deletar_material, name='deletar_material'),
    
    # Atividades
    path('turmas/<int:turma_id>/atividades/criar/', views.criar_atividade, name='criar_atividade'),
    path('atividades/<int:pk>/', views.detalhes_atividade, name='detalhes_atividade'),
    path('atividades/<int:pk>/editar/', views.editar_atividade, name='editar_atividade'),
    
    # Notas
    path('entregas/<int:entrega_id>/avaliar/', views.avaliar_entrega, name='avaliar_entrega'),
    path('turmas/<int:turma_id>/notas/', views.boletim_turma, name='boletim_turma'),
    
    # Avisos
    path('turmas/<int:turma_id>/avisos/criar/', views.criar_aviso, name='criar_aviso'),
]