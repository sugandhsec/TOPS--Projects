from django.http import HttpResponse
from django.shortcuts import render
from app_buyer.models import User
from random import randrange
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'msg': 'User already Exist'})

        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fullname=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                return render(request, "login.html", {'msg': 'Registered Successfully Login Here'})
            else:
                return render(request, 'register.html', {'msg': 'Password Not match'})
    else:
        return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')

