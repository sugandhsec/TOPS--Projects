from django.db import models

# Create your models here.
class User(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    age=models.IntegerField()
    bio=models.CharField(max_length=500)