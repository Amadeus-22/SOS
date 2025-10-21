# [Seu Projeto]/[Seu Projeto]/settings.py

from pathlib import Path
import sys # NOVO: Importação necessária para corrigir o caminho

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-16miwb1_e5^q9sy7@gn4z#l6h3gvsj+%yt&^bcu_7t*jlh2f&j'
DEBUG = True
ALLOWED_HOSTS = []

# --- CORREÇÃO DE ERRO DE MÓDULO (ModuleNotFoundError) ---
# Adiciona o diretório raiz do projeto ao caminho de busca, garantindo que o Django encontre 'atendimento' e 'ong_manager'
sys.path.insert(0, str(BASE_DIR)) 
# Se o seu settings.py está em /SOS/SOS/settings.py, esta linha corrige o problema.
# Se o seu settings.py está em /django_ong/settings.py, esta linha também funciona.


# Application definition

INSTALLED_APPS = [
    # TEMAS E APPS PERSONALIZADOS DEVEM VIR PRIMEIRO
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # SEUS APPS PERSONALIZADOS - CORRIGIDOS AQUI!
    # Usamos o caminho completo para garantir que o Django encontre a AppConfig
    'atendimento.apps.AtendimentoConfig',
    'ong_manager.apps.OngManagerConfig', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Use o nome do seu projeto raiz aqui.
ROOT_URLCONF = 'ong_manager.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Adicionando pasta de templates global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ong_manager.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# Static and Media files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles' 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CONFIGURAÇÕES DE AUTENTICAÇÃO E JAZZMIN ---
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGOUT_REDIRECT_URL = '/'

JAZZMIN_SETTINGS = {
    "site_title": "SOS - Atendimento Social",
    "site_header": "Controle Social ONG",
    "site_brand": "SOS",
    
    "icons": {
        "auth.User": "fas fa-user-cog",
        "auth.Group": "fas fa-users-cog",
        "atendimento.Pessoa": "fas fa-user-friends",
        "atendimento.Atendimento": "fas fa-handshake",
        "atendimento.TipoServico": "fas fa-stethoscope", 
        "ong_manager.DespesaONG": "fas fa-dollar-sign",
        "ong_manager.RegistroPonto": "fas fa-clock",
    },

    "order_with_respect_to": ["auth", "ong_manager", "atendimento"],
    
    "custom_links": {},

    "menu": [
        {"name": "Dashboard Principal", "url": "dashboard", "icon": "fas fa-chart-line"}, 

        {"app": "atendimento", "name": "Fluxo de Atendimento", "icon": "fas fa-clipboard-list", "models": [
            {"model": "atendimento.pessoa", "name": "1. Cadastrar Pessoa"},
            {"model": "atendimento.atendimento", "name": "2. Registrar Atendimento"},
            {"model": "atendimento.tiposervico", "name": "3. Gerenciar Serviços"},
        ]},
        
        {"app": "ong_manager", "name": "Gestão e Controle", "icon": "fas fa-tools", "models": [
            {"model": "ong_manager.despesaong", "name": "1. Módulo Financeiro (Despesas)"},
            {"model": "ong_manager.registroponto", "name": "2. Auditoria de Ponto"},
        ]},

        {"app": "auth", "name": "Sistema e Usuários", "icon": "fas fa-lock"},
    ],

    "theme": "united", 
    "navbar_fixed": True,
    "sidebar_fixed": True,
}

JAZZMIN_UI_TWEAKS = {
    "custom_css": "css/custom_admin.css", 
    "theme": "united",
    "navbar_fixed": True,
    "sidebar_fixed": True,
}