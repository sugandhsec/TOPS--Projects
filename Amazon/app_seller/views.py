from django.shortcuts import render
from app_seller.models import Product, Userseller
import email
from random import randrange
from django.conf import settings
from django.core.mail import send_mail
from app_buyer.models import User
# Create your views here.
def seller_index(request):
    try:
        user_data=Userseller.objects.get(email=request.session['email'])
        return render(request,'seller_index.html',{'user_data': user_data})
    except:   
        return render(request,'seller_index.html',{'msg':'Coming without yuser data'})


def seller_register(request):
    if request.method=="POST":
        try:
            Userseller.objects.get(email=request.POST['email'])
            return render(request,'seller_register.html',{'msg':'Email Already Exist'})
        except:
            if request.POST['password']==request.POST['cpassword']:
                global temp
                temp={
                    'fullname':request.POST['fullname'],
                    'email':request.POST['email'],
                    'mobile':request.POST['mobile'],
                    'password':request.POST['password']
                }
                global otp
                otp=randrange(1000,9999)
                subject = 'OTP FOR REGISTRATION'
                message = f'Hii welcome To My website Your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list =[ request.POST['email'],]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'seller_otp.html')
            else:
                return render(request,'seller_register.html',{'msg':'Password And Confirm Password Not Match'})
    else:
      return render(request,'seller_register.html')  
    
def seller_otp(request):
    if request.method=='POST':
        if int(request.POST['otp'])==otp:
            Userseller.objects.create(
                fullname=temp['fullname'],
                email=temp['email'],
                mobile=temp['mobile'],
                password=temp['password']
            )
            return render(request,'seller_login.html')
        else:
           return render(request,'seller_otp.html',{'msg':'OTP IS WRONG '}) 
    else:
        return render(request,'seller_register.html')

def seller_login(request):
    try:
        request.session['email']
        session_user_data = Userseller.objects.get(email = request.session['email'])
        return render(request,'seller_index.html',{'user_data':session_user_data})
    except:
        if request.method=='POST':
            try:
                session_user=Userseller.objects.get(email=request.POST['email'])
                if request.POST['password']==session_user.password:
                    request.session['email']=request.POST['email']
                    return render(request,'seller_home.html',{'user_data':session_user,'msg':'Welcome To Fruthika'}) 
                else:
                    return render(request,'seller_login.html',{'msg':'Password is Wrong'})
            except:
                return render(request,'seller_login.html',{'msg':'Email is Wrong'}) 
        else:
            return render(request,'seller_login.html')

def seller_profile(request):
    session_user_data = Userseller.objects.get(email = request.session['email'])
    if request.method=="POST":
        if request.FILES:
            session_user_data.fullname=request.POST['fullname']
            session_user_data.mobile=request.POST['mobile']
            session_user_data.password=request.POST['password']
            session_user_data.pic=request.FILES['pic']
            session_user_data.save()
            return render(request,"seller_profile.html",{'user_data':session_user_data,'msg':'Updated Profile Successfully'})
        else:
            session_user_data.fullname=request.POST['fullname']
            session_user_data.mobile=request.POST['mobile']
            session_user_data.password=request.POST['password']
            session_user_data.save()
            return render(request,"seller_profile.html",{'user_data':session_user_data,'msg':'Updated Profile Successfully'})
    return render(request,"seller_profile.html",{'user_data':session_user_data})

def seller_logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request,"seller_login.html",{'msg':'Logged Out Sucessfully'})
    except:
        return render(request,"seller_login.html",{'msg':'Can\'t LogOut Without Login'})
        

def seller_add_product(request):
    session_user_data = Userseller.objects.get(email = request.session['email'])
    if request.method=="POST":
        try:
            Product.objects.get(productname=request.POST['productname'])
            return render(request,'seller_add_product.html',{'msg':'Product Already Exist','user_data':session_user_data})
        except:
            if request.FILES:    
                Product.objects.create(
                    productname=request.POST['productname'],
                    productprice=request.POST['productprice'],
                    productdesc=request.POST['productdesc'],
                    productpic=request.FILES['propic'],
                    seller_id=session_user_data)
                return render(request,'seller_add_product.html',{'msg':'Product Added Successfully','user_data':session_user_data})
            else:
                Product.objects.create(
                    productname=request.POST['productname'],
                    productprice=request.POST['productprice'],
                    productdesc=request.POST['productdesc'],
                    seller_id=session_user_data)

                return render(request,'seller_add_product.html',{'msg':'Product Added Successfully','user_data':session_user_data})
    else:
        return render(request,'seller_add_product.html',{'user_data':session_user_data})  
#get---1 line---condition---only exact one line----error more than1 or less than 1 
#all---all line
#filter---1 se jayda line---condition--more than one line