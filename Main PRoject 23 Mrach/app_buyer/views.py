from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
import random
from .models import *
from app_seller.models import *
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
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
        try:
            image_val=request.FILES["propic"]
        except:
            image_val=data.propic
        if request.POST["oldpassword"]:
            if check_password(request.POST["oldpassword"],data.password):
                if request.POST["newpassword"]==request.POST["cnewpassword"]:
                    data.name=request.POST["name"]
                    data.password=make_password(request.POST["newpassword"])
                    data.propic=image_val
                    data.save()
                    return render(request,"profile.html",{"data":data,"msg":"Profile Update Succesfully"})
                else:
                    return render(request,"profile.html",{"data":data,"msg":"New PAsswrod and Confirm New Passwrod Not match"}) 
            else:
               return render(request,"profile.html",{"data":data,"msg":"Old Passwrod Nort Match"}) 
        else:
            data.name=request.POST["name"]
            data.propic=image_val
            data.save()
            return render(request,"profile.html",{"data":data,"msg":"Profile Update Succesfully"})
    else:
        data=User.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"data":data})
    
def show_product(request):
    all_product=Product.objects.all()
    return render(request,"shop.html",{"all_product":all_product})

def single_product(request,pk):
    one_product=Product.objects.get(id=pk)
    return render(request,"shop-details.html",{"one_product":one_product})

def search(request):
     if request.method=="POST":
        query = request.POST['ser']
        all_product = Product.objects.filter(Q(pro_name__icontains=query)|Q(pro_desc__icontains=query))
        return render(request,"shop.html",{"all_product":all_product})
     else:
          return show_product(request)
     
def add_to_cart(request,pk):
    data=User.objects.get(email=request.session["email"])
    try:
        exists_data=Cart.objects.get( Q(prd_id=pk) & Q( buyer_id=data.id))
        exists_data.qty+=1
        exists_data.total=exists_data.qty*exists_data.prd_id.pro_price
        exists_data.save()
        return single_product(request,pk)
    except:
        product=Product.objects.get(id=pk)
        Cart.objects.create(
            prd_id=product,
            buyer_id=data,
            qty=1,
            total=product.pro_price
        )
        return single_product(request,pk)
    
def show_cart(request):
    data=User.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=data.id)
    final_total=0
    for i in all_cart:
        final_total=final_total+i.total
    return render(request,"shopping-cart.html",{"all_cart":all_cart,"final_total":final_total})


def remove_cart(request,pk):
    one_cart=Cart.objects.get(id=pk)
    one_cart.delete()
    return show_cart(request)

def update_cart(request):
    if request.method=="POST":
        l1=request.POST.getlist("uqty")
        all_cart=Cart.objects.all()
        for i,j in zip(all_cart,l1):
            i.qty=j
            i.total=int(j)*i.prd_id.pro_price
            i.save()
        return show_cart(request)
    else:
        return show_cart(request)
    

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()
