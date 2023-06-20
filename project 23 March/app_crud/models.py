from django.db import models

# Create your models here.
class User(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField()
    passowrd=models.CharField(max_length=80)

    def __str__(self):
        return self.firstname+" " +self.email