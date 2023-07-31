from django.db import models

# Create your models here.
class User(models.Model):
    firstname=models.CharField( max_length=50)
    email= models.EmailField( max_length=254)
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)