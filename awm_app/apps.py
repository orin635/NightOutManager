from django.apps import AppConfig


class AwmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'awm_app'

    def ready(self):
        import awm_app.signals