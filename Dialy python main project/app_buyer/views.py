from django.shortcuts import render
from app_buyer.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password,make_password

# Create your views here.
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST["email"])
            return render(request,"register.html",{"msg":"User Already Exist"})
        except:
            if request.POST["pwd"]==request.POST["cpwd"]:
                global temp
                temp={
                    "firstname":request.POST["name"],
                    "email":request.POST["email"],
                    "phone":request.POST["phone"],
                    "password":request.POST["pwd"]
                }
                import random
                global myotp
                myotp=random.randint(100000,999999)
                subject = 'OTP VERIFICATION'
                message = f'Hii welcome your otp is {myotp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST["email"], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,"otp.html")
            else:
                return render(request,"register.html",{"msg":"Password and confirm password Not Match"})
    else:
        return render(request,"register.html")
    

def otp(request):
    if request.method=="POST":
        if myotp==int(request.POST["otp"]):
            User.objects.create(
                firstname=temp["firstname"],
                email=temp["email"],
                password=make_password(temp["password"]),
                phone=temp["phone"]
            )
            return render(request,"register.html",{"msg":"Registration Successfull"})
        else:
            return render(request,"otp.html",{"msg":"OTP not MATCH"})
    else:
        return render(request,"register.html")