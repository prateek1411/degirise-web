from django.apps import AppConfig


class WebappConfig(AppConfig):
    name = 'webApp'

    def ready(self):
        import webApp.signals
