# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Turma, Aluno, Material, Atividade, Entrega, Nota, Aviso
from .forms import (TurmaForm, AlunoForm, MaterialForm, AtividadeForm, 
                    NotaForm, AvisoForm)

@login_required
def dashboard(request):
    turmas = Turma.objects.filter(professor=request.user).annotate(
        total_alunos=Count('alunos'),
        total_atividades=Count('atividades')
    )
    
    atividades_recentes = Atividade.objects.filter(
        turma__professor=request.user
    ).order_by('-criado_em')[:5]
    
    entregas_pendentes = Entrega.objects.filter(
        atividade__turma__professor=request.user,
        status='ENTREGUE'
    ).count()
    
    context = {
        'turmas': turmas,
        'atividades_recentes': atividades_recentes,
        'entregas_pendentes': entregas_pendentes,
        'total_turmas': turmas.count(),
    }
    return render(request, 'escola/dashboard.html', context)


@login_required
def lista_turmas(request):
    turmas = Turma.objects.filter(professor=request.user).annotate(
        total_alunos=Count('alunos')
    )
    return render(request, 'escola/lista_turmas.html', {'turmas': turmas})


@login_required
def criar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.professor = request.user
            turma.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('escola:detalhes_turma', pk=turma.pk)
    else:
        form = TurmaForm()
    return render(request, 'escola/form_turma.html', {'form': form})


@login_required
def detalhes_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk, professor=request.user)
    alunos = turma.alunos.all()
    materiais = turma.materiais.all()[:5]
    atividades = turma.atividades.all()[:5]
    avisos = turma.avisos.all()[:5]
    
    context = {
        'turma': turma,
        'alunos': alunos,
        'materiais': materiais,
        'atividades': atividades,
        'avisos': avisos,
    }
    return render(request, 'escola/detalhes_turma.html', context)


@login_required
def editar_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk, professor=request.user)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('escola:detalhes_turma', pk=turma.pk)
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'escola/form_turma.html', {'form': form, 'turma': turma})


@login_required
def lista_alunos(request):
    alunos = Aluno.objects.filter(turmas__professor=request.user).distinct()
    return render(request, 'escola/lista_alunos.html', {'alunos': alunos})


@login_required
def criar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, user=request.user)
        if form.is_valid():
            aluno = form.save()
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('escola:detalhes_aluno', pk=aluno.pk)
    else:
        form = AlunoForm(user=request.user)
    return render(request, 'escola/form_aluno.html', {'form': form})


@login_required
def detalhes_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk, turmas__professor=request.user)
    entregas = aluno.entregas.select_related('atividade', 'nota').all()
    
    context = {
        'aluno': aluno,
        'entregas': entregas,
    }
    return render(request, 'escola/detalhes_aluno.html', context)


@login_required
def criar_material(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, professor=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.turma = turma
            material.save()
            messages.success(request, 'Material adicionado com sucesso!')
            return redirect('escola:detalhes_turma', pk=turma.pk)
    else:
        form = MaterialForm()
    return render(request, 'escola/form_material.html', {'form': form, 'turma': turma})


@login_required
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk, turma__professor=request.user)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material atualizado com sucesso!')
            return redirect('escola:detalhes_turma', pk=material.turma.pk)
    else:
        form = MaterialForm(instance=material)
    return render(request, 'escola/form_material.html', {'form': form, 'material': material})


@login_required
def deletar_material(request, pk):
    material = get_object_or_404(Material, pk=pk, turma__professor=request.user)
    turma_id = material.turma.pk
    material.delete()
    messages.success(request, 'Material deletado com sucesso!')
    return redirect('escola:detalhes_turma', pk=turma_id)


@login_required
def criar_atividade(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, professor=request.user)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.turma = turma
            atividade.save()
            messages.success(request, 'Atividade criada com sucesso!')
            return redirect('escola:detalhes_atividade', pk=atividade.pk)
    else:
        form = AtividadeForm()
    return render(request, 'escola/form_atividade.html', {'form': form, 'turma': turma})


@login_required
def detalhes_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk, turma__professor=request.user)
    entregas = atividade.entregas.select_related('aluno', 'nota').all()
    
    context = {
        'atividade': atividade,
        'entregas': entregas,
    }
    return render(request, 'escola/detalhes_atividade.html', context)


@login_required
def editar_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk, turma__professor=request.user)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada com sucesso!')
            return redirect('escola:detalhes_atividade', pk=atividade.pk)
    else:
        form = AtividadeForm(instance=atividade)
    return render(request, 'escola/form_atividade.html', {'form': form, 'atividade': atividade})


@login_required
def avaliar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id, 
                                atividade__turma__professor=request.user)
    
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.entrega = entrega
            nota.save()
            entrega.status = 'AVALIADO'
            entrega.save()
            messages.success(request, 'Entrega avaliada com sucesso!')
            return redirect('escola:detalhes_atividade', pk=entrega.atividade.pk)
    else:
        try:
            nota_existente = entrega.nota
            form = NotaForm(instance=nota_existente)
        except Nota.DoesNotExist:
            form = NotaForm()
    
    context = {
        'form': form,
        'entrega': entrega,
    }
    return render(request, 'escola/form_nota.html', context)


@login_required
def boletim_turma(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, professor=request.user)
    alunos = turma.alunos.all()
    
    boletim = []
    for aluno in alunos:
        notas = Nota.objects.filter(
            entrega__aluno=aluno,
            entrega__atividade__turma=turma
        )
        media = notas.aggregate(Avg('valor'))['valor__avg'] or 0
        
        boletim.append({
            'aluno': aluno,
            'notas': notas,
            'media': round(media, 2)
        })
    
    context = {
        'turma': turma,
        'boletim': boletim,
    }
    return render(request, 'escola/boletim_turma.html', context)


@login_required
def criar_aviso(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, professor=request.user)
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.turma = turma
            aviso.save()
            messages.success(request, 'Aviso criado com sucesso!')
            return redirect('escola:detalhes_turma', pk=turma.pk)
    else:
        form = AvisoForm()
    return render(request, 'escola/form_aviso.html', {'form': form, 'turma': turma})