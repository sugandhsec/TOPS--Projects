from django.db import models

# Create your models here.


class Seller(models.Model):
    password = models.CharField(max_length=30)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    emailid = models.EmailField()
    profilepic = models.FileField(
        upload_to="profile_pic/", default="anonymous.png")

    def __str__(self) -> str:
        return self.firstname
    
class Products(models.Model):
    product_name=models.CharField(max_length=50)
    product_desc=models.TextField()
    product_price=models.IntegerField()
    product_seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    product_image = models.FileField(
        upload_to="product_image/", default="anonymous.png")
# sepcial methods---magic methods
    def __str__(self) -> str:
        return self.product_name


