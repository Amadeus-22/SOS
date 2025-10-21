# ong_manager/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RegistroPonto, DespesaONG
from atendimento.models import Atendimento 
from django.utils import timezone
from django.db.models import Sum

class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request):
        hoje = timezone.now()
        
        is_admin = request.user.is_superuser or request.user.groups.filter(name='Administrador ONG').exists()
        
        if is_admin:
            total_atendimentos = Atendimento.objects.count()
            
            despesas_mes = DespesaONG.objects.filter(
                data__year=hoje.year, data__month=hoje.month
            ).aggregate(Sum('valor'))['valor__sum'] or 0.00
            
            context = {
                'perfil': 'Administrador ONG',
                'total_atendimentos': total_atendimentos,
                'despesas_mes': despesas_mes,
                'template_name': 'ong_manager/dashboard_admin.html'
            }
        
        else:
            atendimentos_hoje = Atendimento.objects.filter(
                profissional_responsavel=request.user, 
                data_atendimento__date=hoje.date()
            ).select_related('pessoa_atendida', 'servico_principal')

            ultimo_registro = RegistroPonto.objects.filter(funcionario=request.user).order_by('-timestamp').first()
            
            status_ponto = "Nenhum ponto registrado."
            if ultimo_registro:
                status_ponto = f"Último: {ultimo_registro.get_tipo_display()} às {ultimo_registro.timestamp.strftime('%H:%M')}"
            
            context = {
                'perfil': 'Profissional de Atendimento',
                'atendimentos_hoje': atendimentos_hoje,
                'status_ponto': status_ponto,
                'template_name': 'ong_manager/dashboard_profissional.html'
            }

        return render(request, 'ong_manager/dashboard.html', context)
        
class RegistroPontoView(LoginRequiredMixin, View):
    
    def post(self, request):
        tipo = request.POST.get('tipo_ponto')
        localizacao = request.POST.get('localizacao', 'Não informada') 
        
        RegistroPonto.objects.create(
            funcionario=request.user,
            tipo=tipo,
            localizacao_gps=localizacao
        )
        return redirect('dashboard')