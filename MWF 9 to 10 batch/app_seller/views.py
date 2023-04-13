from django.shortcuts import render
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from app_seller.models import *

# Create your views here.
def seller_index(request):
    return render (request,"seller_index.html")

def seller_register(request):
    if request.method == "POST":
        try:
            seller_user.objects.get(email= request.POST['email'])
            return render(request,"seller_register.html",{'msg':"user already exist"})
        except:
            if request.POST["pass"]==request.POST["cpass"]:
                global temp
                temp = {
                    'fname':request.POST["fname"],
                    'email':request.POST["email"],
                    'pass':make_password(request.POST["pass"])
                }
                global votp
                votp=random.randint(100,999)
                subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
                message = f'YOUR OTP IS  {votp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'],]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,"seller_otp.html")
            else:
                return render(request,"seller_register.html",{'msg':"password and confirm password is not match"})
    else:
        return render (request,"seller_register.html")
    

def seller_otp(request):
    if request.method=="POST":
        if votp == int(request.POST['OTP']):
            seller_user.objects.create(
                fullname = temp['fname'],
                email = temp['email'],
                password = temp['pass']
            )
            return render(request,"seller_login.html",{'msg':'Registraion Sucessfully'})
        else:
            return render (request,"seller_otp.html",{'msg':'OTP is INCORRECT'})
    else:
        return render(request,"seller_otp.html")


def seller_login(request):
    if request.method=="POST":
        try:
            user_data=seller_user.objects.get(email= request.POST["email"])
            if check_password(request.POST["pass"],user_data.password):
                request.session['email']=request.POST["email"]
                request.session['name']=user_data.fullname
                return render (request, "seller_homepage.html")
            else:
                return render(request,"seller_login.html" , {"msg":"password is incorrect"})
        except:
            return render(request,"seller_login.html" , {"msg":"you email is not register"})
    else:
        return render(request,"seller_login.html")
    

def seller_forgot_password(request):
    if request.method == "POST":
        try:
            user_data=seller_user.objects.get(email= request.POST["email"])
            request.session['e_email']=request.POST["email"]
            global votp
            votp=random.randint(100000,999999)
            subject = 'EVIB ECOMMERCE OTP VERIFICATION MAIL'
            message = f'YOUR OTP IS  {votp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'],]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,"seller_forgot_otp.html")
        except:
            return render(request,"seller_forgot_password.html", {"msg":"your email is not register please register first"})
    else:
        return render (request,"seller_forgot_password.html")
    

def seller_reset_password(request):
    if request.method == "POST":
        if request.POST["pass"]==request.POST["cpass"]:
            user_data=seller_user.objects.get(email=request.session['e_email'])
            user_data.password=make_password(request.POST["pass"])
            user_data.save()
            return render(request,"seller_homepage.html",{'msg':'password reset Sucessfully'})
        else:
        
            return render(request,"seller_reset_password.html",{"msg":"password not match"})
    else:
        return render(request,"seller_reset_password.html")
    

    

def seller_forgot_otp(request):
    if request.method=="POST":
        if votp == int(request.POST['OTP']):
            return render(request,"seller_reset_password.html",{'msg':'Registraion Sucessfully'})
        else:
            return render (request,"seller_forgot_otp.html",{'msg':'OTP is INCORRECT'})
    else:
        return render(request,"seller_forgot_otp.html")