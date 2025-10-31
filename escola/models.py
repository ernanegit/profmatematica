# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    descricao = models.TextField(blank=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turmas')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Turmas"
        ordering = ['-ano', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.ano}"


class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    turmas = models.ManyToManyField(Turma, related_name='alunos')
    data_nascimento = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Alunos"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class Material(models.Model):
    TIPO_CHOICES = [
        ('PDF', 'PDF'),
        ('VIDEO', 'Vídeo'),
        ('LINK', 'Link'),
        ('DOCUMENTO', 'Documento'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='materiais/', null=True, blank=True)
    link = models.URLField(blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='materiais')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Materiais"
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.titulo


class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='atividades')
    data_entrega = models.DateTimeField()
    valor_pontos = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    arquivo_anexo = models.FileField(upload_to='atividades/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Atividades"
        ordering = ['-data_entrega']
    
    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"


class Entrega(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENTREGUE', 'Entregue'),
        ('AVALIADO', 'Avaliado'),
        ('ATRASADO', 'Atrasado'),
    ]
    
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='entregas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='entregas')
    arquivo = models.FileField(upload_to='entregas/', null=True, blank=True)
    comentario_aluno = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_entrega = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Entregas"
        unique_together = ['atividade', 'aluno']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.titulo}"


class Nota(models.Model):
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, related_name='nota')
    valor = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    comentario_professor = models.TextField(blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Notas"
    
    def __str__(self):
        return f"{self.entrega.aluno.nome} - {self.valor}"


class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='avisos')
    importante = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Avisos"
        ordering = ['-importante', '-criado_em']
    
    def __str__(self):
        return self.titulo