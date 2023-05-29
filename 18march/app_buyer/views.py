from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
# Create your views here.
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method=="POST":
        if request.POST["cpassword"]== request.POST["password"]:
            import random
            global user_otp
            user_otp=random.randint(100000,999999)
            subject = 'OTP VERIFICATION PROCESS FOR JEWEL WORLD'
            message = f'thanks For choosing us your otp is {user_otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST["email"], ]
            send_mail( subject, message, email_from, recipient_list )
            global temp
            temp={
                "firstname":request.POST["fname"],
                "lastname":request.POST["lname"],
                "email":request.POST["email"],
                "password":request.POST["password"],
            }
            return render(request,"otp.html")
        else:
            return render(request,"register.html",{"msg":"Password And confirm password not match"})
    else:
        return render(request,"register.html") 

def otp(request):
    if request.method=="POST":
        if user_otp==int(request.POST["otp"]):
            User.objects.create(
                firstname=temp["firstname"],
                lastname=temp["lastname"],
                email=temp["email"],
                password=make_password(temp["password"])
            )
            return render(request,"register.html",{"msg":"registration Succesfull"})
        else:
            return render(request,"otp.html",{"msg":"OTP NOT MATCHED"})
    else:
        return render(request,"register.html")