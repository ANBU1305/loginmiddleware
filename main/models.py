from mongoengine import Document, StringField, EmailField, DictField, ListField, ReferenceField
from mongoengine.fields import EmbeddedDocumentField
from mongoengine import EmbeddedDocument

# You won't use django.contrib.auth.models.User directly,
# instead, define your own User document or link with ObjectId.

class User(Document):
    # Simplified user document for example
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    # add other fields as needed

class UserLogin(Document):
    user = ReferenceField(User, required=True, unique=True)  # like OneToOneField
    name = StringField(max_length=100, required=True)
    email = EmailField(required=True)
    address = DictField()  # for JSON-like data
    hobbies = ListField(StringField())  # for a list of hobbies
    
    def __str__(self):
        return self.name
