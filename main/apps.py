from django.apps import AppConfig

from mongoengine import connect

connect(
    db='LoginMiddlware',  # your database name
    host='mongodb+srv://anbumay131998_db_user:ywdQxMyY22zXzV6d@loginmiddlware.bpn4a0i.mongodb.net/LoginMiddlware?retryWrites=true&w=majority'
)



class MainConfig(AppConfig):
    name = 'main'
