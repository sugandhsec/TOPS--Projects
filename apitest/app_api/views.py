from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_api.models import Employee
from app_api.serializers import Employeeserial

# Create your views here.
def index(request):
    return render(request,"index.html")

	# Create your views here.
@api_view(['GET'])
def getemployees(request):
        emplist=Employee.objects.all()
        serial = Employeeserial(emplist,many=True)
        return Response(serial.data)
