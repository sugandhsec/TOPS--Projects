from django.db import models
from app_seller.models import  *

# Create your models here.
class User(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    profilepic = models.FileField(upload_to='media/',default="anonymous.jfif")

    def __str__(self):
        return self.fullname
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.quantity)+" "+self.product.pname
