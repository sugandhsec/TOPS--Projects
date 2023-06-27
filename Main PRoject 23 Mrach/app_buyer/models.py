from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    propic=models.FileField(upload_to="media/",default="anonymous.jpg")

    