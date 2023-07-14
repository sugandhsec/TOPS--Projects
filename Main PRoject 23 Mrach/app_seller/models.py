from django.db import models

# Create your models here.
class Seller_user(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    propic=models.FileField(upload_to="media/",default="anonymous.jpg")

class Product(models.Model):
    pro_name=models.CharField(max_length=50)
    pro_price=models.IntegerField()
    pro_qty=models.IntegerField()
    pro_image=models.FileField(upload_to="Product/",default="pro.jpg")
    pro_desc=models.TextField(max_length=500)
    seller_id=models.ForeignKey(Seller_user,on_delete=models.CASCADE)