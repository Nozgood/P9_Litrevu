from django.apps import AppConfig


class LitrevuManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'litrevu_management'

    def ready(self):
        import litrevu_management.signals
