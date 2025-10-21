# ong_manager/apps.py

from django.apps import AppConfig

class OngManagerConfig(AppConfig): # O nome da classe deve ser este
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ong_manager'
    verbose_name = '3. Gestão e Controle'