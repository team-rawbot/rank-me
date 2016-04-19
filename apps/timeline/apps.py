from django.apps import AppConfig


class TimelineConfig(AppConfig):
    name = 'apps.timeline'

    def ready(self):
        from .signals import handlers  # NOQA
