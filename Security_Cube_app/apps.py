from django.apps import AppConfig


class SecurityCubeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Security_Cube_app'

    def ready(self):
        import Security_Cube_app.signals
