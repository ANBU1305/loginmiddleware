# In your app's models.py

from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.JSONField()
    hobbies = models.JSONField()
    
    def __str__(self):
        return self.name