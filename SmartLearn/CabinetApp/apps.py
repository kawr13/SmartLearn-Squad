from django.apps import AppConfig


class CabinetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CabinetApp'

    def ready(self):
        import CabinetApp.signals
