from django.db import models
from app_seller.models import *

# Create your models here.


class User(models.Model):
    password = models.CharField(max_length=30)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    emailid = models.EmailField()
    profilepic=models.FileField(upload_to="profile_pic/",default="anonymous.png")

    def __str__(self) -> str:
        return self.firstname

class Cart(models.Model):
    product_detail=models.ForeignKey(Products,on_delete=models.CASCADE)
    buyer_detail=models.ForeignKey(User,on_delete=models.CASCADE)
    cart_time=models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return self.product_detail.product_name
