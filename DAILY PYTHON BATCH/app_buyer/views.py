from django.shortcuts import render
from app_buyer.models import *
# Create your views here.
def index(request):
    return render(request,"index.html")


def dataentry(request):
    if request.method=="POST":
        User.objects.create(
            firstname=request.POST["fname"],
            lastname=request.POST["lname"],
            email=request.POST["email"],
            password=request.POST["pwd"],
            age=request.POST["age"],
            bio=request.POST["bio"]
        )
        return render(request,"index.html",{"msg":"Data Added Successfully"})
    else:
        return render(request,"index.html")
    
def showdata(request):
    all_data=User.objects.all()
    return render(request,"data.html",{"all_data":all_data})

