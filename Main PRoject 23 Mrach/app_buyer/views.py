from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
import random
from .models import *
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=="POST":
        if request.POST["password"]==request.POST["cpassword"]:
            global temp
            temp={
                "name":request.POST["name"],
                "email":request.POST["email"],
                "password":request.POST["password"]
            }
            global a
            a=random.randint(10000000,99999999)
            subject = 'OTP VERIFICATION FOR MY WEBSITE'
            message = f'Your OTP IS {a} Valid for 5 mintutes only'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST["email"], ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,"otp.html")

        else:
           return render(request,"sign.html",{"msg":"Passwordod And confirm passwrod Not MAtch"})  
    else:
        return render(request,"sign.html")
    
def otp(request):
    if request.method=="POST":
        if a==int(request.POST["otp"]):
           User.objects.create(
               name=temp["name"],
               email=temp["email"],
               password=make_password(temp["password"])
           )
           return render(request,"sign.html",{"msg":"Registration Succesfukll"}) 
        else:
            return render(request,"otp.html",{"msg":"OTP NOT MATCHED"})

    else:
        return render(request,"sign.html")
    

def login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                request.session["email"]=request.POST["email"]
                return render(request,"shop.html")
            else:
                return render(request,"login.html",{"msg":"Password Not Match"})

        except:
            return render(request,"login.html",{"msg":"User not Exist"})
            
    else:
        return render(request,"login.html")
    
def logout(request):
    del request.session["email"]
    return render(request,"login.html",{"msg":"Logout Successfully"})

def profile(request):
    data=User.objects.get(email=request.session["email"])
    if request.method=="POST":
        if request.POST["oldpassword"]:
            if check_password(request.POST["oldpassword"],data.password):
                if request.POST["newpassword"]==request.POST["cnewpassword"]:
                    data.name=request.POST["name"]
                    data.password=make_password(request.POST["newpassword"])
                    data.save()
                    return render(request,"profile.html",{"data":data,"msg":"Profile Update Succesfully"})
                else:
                    return render(request,"profile.html",{"data":data,"msg":"New PAsswrod and Confirm New Passwrod Not match"}) 
            else:
               return render(request,"profile.html",{"data":data,"msg":"Old Passwrod Nort Match"}) 
        else:
            data.name=request.POST["name"]
            data.save()
            return render(request,"profile.html",{"data":data,"msg":"Profile Update Succesfully"})
    else:
        data=User.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"data":data})