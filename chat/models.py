from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now=True)
    body = models.CharField(max_length=250)
    
    def __str__(self):
        return self.body

