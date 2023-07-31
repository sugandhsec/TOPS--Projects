from rest_framework import serializers
from .models import *

class UserSerial(serializers.ModelSerializer):
    class Meta:
        model  =  User
        fields  = '__all__'
