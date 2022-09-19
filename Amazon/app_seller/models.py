from django.db import models

# Create your models here.
class Userseller(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    pic=models.FileField(upload_to='buyer_images',default="anonymous.png")

    def __str__(self):
        return self.email

class Product(models.Model):
    productname=models.CharField(max_length=50)
    productprice=models.CharField(max_length=10)
    productdesc=models.CharField(max_length=500)
    productpic=models.FileField(upload_to='product_images',default='anonymous.png')
    seller_id=models.ForeignKey(Userseller,on_delete=models.CASCADE)

    def __str__(self):
        return self.productname