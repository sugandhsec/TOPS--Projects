from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=60)
    mobile=models.CharField(max_length=12)

    def __str__(self):
        return self.name