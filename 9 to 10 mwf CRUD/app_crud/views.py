from django.shortcuts import render
from app_crud.models import *
# Create your views here.

def index(request):
    user_data=User.objects.all()
    return render(request,"index.html",{"user_data":user_data})

def dataentry(request):
    if request.method=="POST":
        User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile']
        )
        user_data=User.objects.all()
        return render(request,"index.html",{"msg":"Entry Created","user_data":user_data})
    

def update(request,pk):
    if request.method=="POST":
        one_user_data=User.objects.get(id=pk)
        one_user_data.name=request.POST['name']
        one_user_data.email=request.POST['email']
        one_user_data.mobile=request.POST['mobile']
        one_user_data.save()
        user_data=User.objects.all()
        return render(request,"index.html",{"msg":"Updated Suceesfully","user_data":user_data})
    else:
        user_data=User.objects.all()
        one_user_data=User.objects.get(id=pk)
        return render(request,"update.html",{"one_user_data":one_user_data,"user_data":user_data})
    
def delete(request,pk):
    user_value=User.objects.get(id=pk)
    user_value.delete()
    user_data=User.objects.all()
    return render(request,"index.html",{"msg":"Deleted Suceesfully","user_data":user_data})

        
"""
get---tablename.objects.get(condition) --one
filter---tablename.objects.filter(condition) --one or many
all---tablename.objects.all() -all
"""