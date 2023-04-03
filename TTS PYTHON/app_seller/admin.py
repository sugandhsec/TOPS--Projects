from django.contrib import admin
from app_seller import models
# Register your models here.
admin.site.register(models.Seller),
admin.site.register(models.Products)
