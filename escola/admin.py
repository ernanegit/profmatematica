from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Turma, Aluno, Material, Atividade, Entrega, Nota, Aviso

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'professor', 'criado_em']
    list_filter = ['ano', 'professor']
    search_fields = ['nome', 'descricao']
    date_hierarchy = 'criado_em'


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'matricula', 'email', 'criado_em']
    search_fields = ['nome', 'matricula', 'email']
    filter_horizontal = ['turmas']
    date_hierarchy = 'criado_em'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'turma', 'criado_em']
    list_filter = ['tipo', 'turma']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'criado_em'


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'turma', 'data_entrega', 'valor_pontos', 'criado_em']
    list_filter = ['turma', 'data_entrega']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_entrega'


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'atividade', 'status', 'data_entrega']
    list_filter = ['status', 'atividade__turma']
    search_fields = ['aluno__nome', 'atividade__titulo']
    date_hierarchy = 'data_entrega'


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ['get_aluno', 'get_atividade', 'valor', 'data_avaliacao']
    list_filter = ['entrega__atividade__turma', 'data_avaliacao']
    search_fields = ['entrega__aluno__nome']
    
    def get_aluno(self, obj):
        return obj.entrega.aluno.nome
    get_aluno.short_description = 'Aluno'
    
    def get_atividade(self, obj):
        return obj.entrega.atividade.titulo
    get_atividade.short_description = 'Atividade'


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'turma', 'importante', 'criado_em']
    list_filter = ['importante', 'turma']
    search_fields = ['titulo', 'conteudo']
    date_hierarchy = 'criado_em'