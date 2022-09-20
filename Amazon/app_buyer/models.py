import email
from django.db import models

from app_seller.models import Product

# Create your models here.


class User(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='buyer_images', default="anonymous.png")

    def __str__(self):
        return self.email


class Cart(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    prodcutid = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderid = models.IntegerField()

    def __str__(self):
        return str(self.orderid)
