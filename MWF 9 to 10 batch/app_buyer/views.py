from django.shortcuts import render
from app_buyer.models import *
import random
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            return render(request, "register.html", {'msg': "User already Exist"})
        except:
            if request.POST['pass'] == request.POST['cpass']:
                global temp
                temp = {
                    'fname': request.POST['fname'],
                    'email': request.POST['email'],
                    'pass': request.POST['pass']
                }
                global votp
                votp = random.randint(100000, 999999)
                subject = 'EVIB ECOMMERECE OTP VERIFICATION MAIL'
                message = f'Your OTP IS {votp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, "otp.html")
            else:
                return render(request, "register.html", {'msg': "Password And Confirm Password Not match"})
    else:
        return render(request, "register.html")


def otp(request):
    if request.method == "POST":
        print(type(votp), type(request.POST['otp']))
        if votp == int(request.POST['otp']):
            User.objects.create(
                fullname=temp['fname'],
                email=temp['email'],
                password=temp['pass']
            )
            return render(request, "login.html", {'msg': "Registration SUccessful"})
        else:
            return render(request, "otp.html", {'msg': "OTP INCORRECT"})
    else:
        return render(request, "otp.html")
