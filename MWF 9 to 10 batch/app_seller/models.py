from django.db import models

# Create your models here.


class seller_user(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname
