# ong_manager/urls.py (O arquivo que é seu ROOT_URLCONF)

from django.contrib import admin
from django.urls import path, include
from .views import DashboardView, RegistroPontoView 
# NÃO use a importação 'from django.conf.urls.static import static' aqui! 
# Use-a apenas no arquivo de URLs que está no seu settings.py (o raiz).

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('accounts/', include('django.contrib.auth.urls')),
    
    # ROTA DO SEU APP DE ATENDIMENTO
    path('atendimento/', include('atendimento.urls')), # Chame o arquivo limpo
    
    # ROTAS DO SEU APP ONG_MANAGER (Dashboard e Ponto)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ponto/registrar/', RegistroPontoView.as_view(), name='registro_ponto'),
]