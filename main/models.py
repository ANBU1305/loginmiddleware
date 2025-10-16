# authentication_api/models.py

from mongoengine import Document, StringField, EmailField, DictField, ListField, ReferenceField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # For now, store raw or hashed manually
    email = EmailField(required=True, unique=True)

class UserLogin(Document):
    user = ReferenceField(User, required=True, unique=True)  # Like OneToOne
    name = StringField(max_length=100, required=True)
    email = EmailField(required=True)
    address = DictField()
    hobbies = ListField(StringField())

    def __str__(self):
        return self.name
