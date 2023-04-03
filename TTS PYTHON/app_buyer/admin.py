from django.contrib import admin
from app_buyer import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Cart)