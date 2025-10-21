# ong_manager/admin.py
from django.contrib import admin
from .models import RegistroPonto, DespesaONG
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Função auxiliar para permissão customizada
def get_financeiro_permission():
    content_type = ContentType.objects.get_for_model(DespesaONG)
    permission, created = Permission.objects.get_or_create(
        codename='view_financeiro',
        name='Pode visualizar o módulo financeiro',
        content_type=content_type,
    )
    return permission

@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'tipo', 'timestamp')
    list_filter = ('funcionario', 'tipo', 'timestamp')
    search_fields = ('funcionario__username',)
    readonly_fields = ('timestamp',) 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Administrador ONG').exists():
            return qs
        return qs.filter(funcionario=request.user)


@admin.register(DespesaONG)
class DespesaONGAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria')
    list_filter = ('categoria', 'data')
    search_fields = ('descricao',)
    
    # Restringe a visibilidade do Módulo Despesas (Financeiro)
    def has_module_permission(self, request):
        perm = get_financeiro_permission()
        return request.user.has_perm(f'{perm.content_type.app_label}.{perm.codename}') or request.user.is_superuser

    # Preenche 'registrado_por'
    def save_model(self, request, obj, form, change):
        if not change:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)