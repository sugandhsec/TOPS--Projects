from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
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
    

def login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],user_data.password):
                request.session["email"]=request.POST["email"]
                return render(request,"four-col.html",{"data":request.session["email"]})
            else:
                return render(request,"login.html",{"msg":"Passwrod Not match"})
        except:
            return render(request,"login.html",{"msg":"We cannot find an account with that email address"})
    else:
        return render(request,"login.html")
    
def logout(request):
    del request.session["email"]
    return render(request,"login.html",{"msg":"Logout Suceesfull"})

def profile(request):
    user_data=User.objects.get(email=request.session["email"])
    return render(request,"profile.html",{"user_data":user_data,"data":request.session["email"]})

def update_profile(request):
    if request.method=="POST":
        user_data=User.objects.get(email=request.session["email"])
        try:
            request.FILES["propic"]
            try:
                request.POST["npassword"]
                if check_password(request.POST["opassword"],user_data.password):
                    if request.POST["cpassword"]==request.POST["npassword"]:
                            user_data.firstname=request.POST["fname"]
                            user_data.lastname=request.POST["lname"]
                            user_data.password=make_password(request.POST["npassword"])
                            user_data.profile_pic=request.FILES["propic"]
                            user_data.save()
                    else:
                        return render(request,"profile.html",{"user_data":user_data,"msg":"New Password and Confrim Password Not Match","data":request.session["email"]})
                else:
                    return render(request,"profile.html",{"user_data":user_data,"msg":"Old PAsswrod Not match","data":request.session["email"]})
            except:
                user_data.firstname=request.POST["fname"]
                user_data.lastname=request.POST["lname"]
                user_data.profile_pic=request.FILES["propic"]
                user_data.save()
            return render(request,"profile.html",{"user_data":user_data,"msg":"Profile Updated Successfully","data":request.session["email"]})
        except:
            try:
                request.POST["npassword"]
                if check_password(request.POST["opassword"],user_data.password):
                    if request.POST["cpassword"]==request.POST["npassword"]:
                            user_data.firstname=request.POST["fname"]
                            user_data.lastname=request.POST["lname"]
                            user_data.password=make_password(request.POST["npassword"])
                            user_data.save()
                    else:
                        return render(request,"profile.html",{"user_data":user_data,"msg":"New Password and Confrim Password Not Match","data":request.session["email"]})
                else:
                    return render(request,"profile.html",{"user_data":user_data,"msg":"Old PAsswrod Not match","data":request.session["email"]})
            except:
                user_data.firstname=request.POST["fname"]
                user_data.lastname=request.POST["lname"]
                user_data.save()
            return render(request,"profile.html",{"user_data":user_data,"msg":"Profile Updated Successfully","data":request.session["email"]})
    else:
        user_data=User.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"user_data":user_data,"data":request.session["email"]})
