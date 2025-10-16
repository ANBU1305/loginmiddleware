# main/apps.py

from django.apps import AppConfig
from .db import connect_db  # import the connect function

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        connect_db()
