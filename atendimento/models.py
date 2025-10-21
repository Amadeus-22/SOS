# atendimento/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Pessoa(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco_bairro = models.CharField(max_length=100, verbose_name="Endereço/Bairro")
    cpf = models.CharField(max_length=14, unique=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    frequenta_nova_igreja = models.BooleanField(default=False, verbose_name="Frequenta a Nova Igreja")

    def __str__(self):
        return self.nome

class TipoServico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Tipo de Serviço"
        verbose_name_plural = "Tipos de Serviços"

class Atendimento(models.Model):
    pessoa_atendida = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Pessoa Atendida")
    servico_principal = models.ForeignKey(TipoServico, on_delete=models.SET_NULL, null=True, related_name='atendimentos_principais', verbose_name="Serviço Principal")
    profissional_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Profissional Responsável")
    data_atendimento = models.DateTimeField(default=timezone.now, verbose_name="Data do Atendimento")
    
    queixa = models.TextField(verbose_name="Queixa/Motivo do Atendimento")
    
    servicos_utilizados = models.ManyToManyField(
        TipoServico, 
        related_name='atendimentos_utilizados',
        verbose_name="Equipes/Serviços Utilizados (Múltipla Seleção)"
    )
    
    observacoes_outras = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="OUTROS (Comentários do Formulário)"
    )

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"

    def __str__(self):
        return f"Atendimento para {self.pessoa_atendida.nome}"