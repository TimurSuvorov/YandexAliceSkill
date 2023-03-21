from django.apps import AppConfig

from mainapp.apscheduler import run_apscheduler


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        run_apscheduler()
