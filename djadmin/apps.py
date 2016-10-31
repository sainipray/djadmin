from django.apps import AppConfig


class ActivityAppConfig(AppConfig):
    name = 'djadmin'

    def ready(self):
        import djadmin.signals
