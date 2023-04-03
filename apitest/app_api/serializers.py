
from rest_framework import serializers
from .models import *

class Employeeserial(serializers.ModelSerializer):
    class Meta:
        model  =  Employee
        fields  = '__all__'