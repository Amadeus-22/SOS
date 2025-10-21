# ong_manager/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

# --- 1. Controle de Ponto ---
class RegistroPonto(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('PI', 'Pausa Início'),
        ('PF', 'Pausa Fim'),
        ('S', 'Saída'),
    ]
    
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    localizacao_gps = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localização (GPS)")

    def __str__(self):
        return f"{self.funcionario.username} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Ponto"
        ordering = ['-timestamp']

# --- 2. Gestão de Despesas (Financeiro) ---
class DespesaONG(models.Model):
    CATEGORIA_CHOICES = [
        ('GAS', 'Gasolina/Transporte'),
        ('SAL', 'Salário/Ajuda de Custo'),
        ('COM', 'Compras/Suprimentos'),
        ('ADM', 'Administrativo'),
        ('OUT', 'Outros'),
    ]
    
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    data = models.DateField(default=timezone.now)
    categoria = models.CharField(max_length=3, choices=CATEGORIA_CHOICES)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Despesa de {self.valor} ({self.get_categoria_display()})"

    class Meta:
        verbose_name = "Despesa da ONG"
        verbose_name_plural = "Despesas da ONG"
        permissions = [
            ("view_financeiro", "Pode visualizar o módulo financeiro"),
        ]