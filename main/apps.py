# main/apps.py

from django.apps import AppConfig
from mongoengine import connect
import os

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # Only connect once when Django is ready
        connect(
            db='LoginMiddlware',
            host='mongodb+srv://anbumay131998_db_user:Zjo5xdFw6PKzysIF@loginmiddlware.bpn4a0i.mongodb.net/LoginMiddlware?retryWrites=true&w=majority'
        )
