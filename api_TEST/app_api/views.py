from http.client import HTTPResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_api import serializers
from app_api.models import Employee
from app_api.serializers import Employeeserial
from rest_framework.views import APIView


# Create your views here.
def api(request):
     return render(request,'index.html')
    
class userList(APIView):
    def get(self,request):
        emplist=Employee.objects.all()
        serializer = Employeeserial(emplist,many=True)
        return Response(serializer.data)