from django.shortcuts import render
from app_buyer.models import *
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=="POST":
        # tablename.objects.get(databasefieldname=request.POST['htmlfieldname'])
        # get method gives error when 0 or more than 1 row is fetched
        try:
            User.objects.get(username=request.POST['email'])
            return render(request,"register.html",{'msg':"User Already Exist"})
        except:
            if request.POST['password']==request.POST['cpassword']:
                global votp
                votp=random.randint(100000,999999)
                subject = 'OTP VERIFICATION EVIB WEBSITE'
                message = f'Hi THANKS FOR CHOOSING YOUR OTP IS {votp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                global temp
                temp={
                    'fname':request.POST['fname'],
                    'uname':request.POST['email'],
                    'pass':request.POST['password']
                }
                return render(request,"otp.html")
            else:
                return render(request,"register.html",{'msg':"Password and Confirm Password Not match"})
    else:   
        return render(request,"register.html")
    
def otp(request):
    if request.method=="POST":
        if votp==int(request.POST['otp']):
            User.objects.create(
                fullname=temp['fname'],
                username=temp['uname'],
                password=temp['pass']
            )
            return render(request,"login.html")
        else:
             return render(request,"otp.html",{'msg':'Invalid OTP'})
    else:
        return render(request,"otp.html")