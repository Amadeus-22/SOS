# atendimento/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group # IMPORTAÇÃO CORRIGIDA
from .models import Pessoa, Atendimento, TipoServico

admin.site.register(TipoServico)

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'genero', 'frequenta_nova_igreja', 'endereco_bairro')
    list_filter = ('genero', 'frequenta_nova_igreja')
    search_fields = ('nome', 'cpf')

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('pessoa_atendida', 'servico_principal', 'profissional_responsavel', 'data_atendimento')
    list_filter = ('servico_principal', 'profissional_responsavel', 'data_atendimento')
    search_fields = ('pessoa_atendida__nome', 'queixa')
    filter_horizontal = ('servicos_utilizados',) 

    fieldsets = (
        (None, {
            'fields': ('pessoa_atendida', 'profissional_responsavel', 'servico_principal')
        }),
        ('Detalhes do Formulário (SOS)', {
            'fields': ('queixa', 'servicos_utilizados', 'observacoes_outras'),
        }),
    )

    # Lógica de Permissão: Profissional só vê o que lhe foi atribuído
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Superuser ou membro do grupo Administrador ONG vê TUDO
        is_admin = request.user.is_superuser or request.user.groups.filter(name='Administrador ONG').exists()
        
        if is_admin:
            return qs
        
        # Membro do grupo Profissional Atendimento vê SÓ os seus
        if request.user.groups.filter(name='Profissional Atendimento').exists():
            return qs.filter(profissional_responsavel=request.user)
            
        return qs.none() # Outros usuários não autorizados não veem nada