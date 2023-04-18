from django.shortcuts import render
from app_crud.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from app_crud.serializers import  *
import requests

# Create your views here.
def index(request):
    if request.method=="POST":
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
        )
        user_data=User.objects.all()
        return render(request,"index.html",{"user_data":user_data})
    else:
        user_data=User.objects.all()
        return render(request,"index.html",{"user_data":user_data})
    
def update(request,pk):
    if request.method=="POST":
        user_value=User.objects.get(id=pk)
        user_value.name=request.POST['name']
        user_value.email=request.POST['email']
        user_value.mobile=request.POST['mobile']
        user_value.save()
        user_data=User.objects.all()
        return render(request,"index.html",{"user_data":user_data})
    else:
        user_data=User.objects.all()
        user_value=User.objects.get(id=pk)
        return render(request,"update.html",{"user_value":user_value,"user_data":user_data})
    
def delete(request,pk):
    user_value=User.objects.get(id=pk)
    user_value.delete()
    user_data=User.objects.all()
    return render(request,"index.html",{"user_data":user_data})

class getuser(APIView):
    def get(self,request):
        user_data=User.objects.all()
        serailized_data=UserSerializer(user_data,many=True)
        return Response(serailized_data.data)

def apidata(request):
    response=requests.get("https://covid-api.com/api/regions").json()
    return render(request,"covid.html",{"response":response})
