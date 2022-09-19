import email
from pyexpat import model
from django.db import models

# Create your models here.
class User(models.Model):
    fullname=models.CharField(max_length=25)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.email
