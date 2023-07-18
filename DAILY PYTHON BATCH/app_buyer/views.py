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
    # for i in all_data:
    #     i.delete()
    return render(request,"data.html",{"all_data":all_data})


def delete(request,pk):
    one_data=User.objects.get(id=pk)
    one_data.delete()
    return showdata(request)


def update(request,pk):
    if request.method=="POST":
        one_data=User.objects.get(id=pk)
        one_data.firstname=request.POST["fname"]
        one_data.lastname=request.POST["lname"]
        one_data.email=request.POST["email"]
        one_data.password=request.POST["pwd"]
        one_data.age=request.POST["age"]
        one_data.bio=request.POST["bio"]
        one_data.save()
        return showdata(request)
    else:
        one_data=User.objects.get(id=pk)
        return render(request,"update.html",{"one_data":one_data})
