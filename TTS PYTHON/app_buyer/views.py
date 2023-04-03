from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import razorpay
import random
from django.shortcuts import render
from app_buyer.models import *
from app_seller.models import *
from django.conf import settings
from django.core.mail import send_mail
rotp = 0


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def checkout(request):
	currency = 'INR'
	amount = 20000  # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'index.html', context=context)


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
				amount = 20000  # Rs. 200
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


# Create your views here.

def index(request):
    return render(request, "index.html")
# sugandhgupta.tops@gmail.com


def register(request):
    if request.method == "POST":
        try:
            User.objects.get(emailid=request.POST['email'])
            return render(request, "register.html", {"msg": "Email Already Exist"})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global temp
                temp = {
                    "email": request.POST['email'],
                    "passw": request.POST['password'],
                    "fname": request.POST['firstname'],
                    "lname": request.POST['lastname']
                }
                global rotp
                rotp = random.randrange(100000, 999999)
                subject = 'OTP AUTHENITICATION'
                message = f'Hi WElcome to tops Your otp is {rotp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, "otp.html")
                # User.objects.create(
                #     password=request.POST['password'],
                #     firstname=request.POST['firstname'],
                #     lastname=request.POST['lastname'],
                #     emailid=request.POST['email']
                # )
                # return render(request, "register.html", {"msg": "Succesfully registered"})
            else:
                return render(request, "register.html", {"msg": "PAssword and Confirmpassword not match"})

    else:
        return render(request, "register.html")


def otp(request):
    if request.method == "POST":
        if int(request.POST['votp']) == rotp:
            User.objects.create(
                firstname=temp['fname'],
                lastname=temp['lname'],
                emailid=temp['email'],
                password=temp['passw']
            )
            return render(request, "login.html")
        else:
            return render(request, "otp.html", {"msg": "OTP NOT VALID"})
    else:
        return render(request, "index.html")


def login(request):
    if request.method == "POST":
        try:
            user_data = User.objects.get(emailid=request.POST['email'])
            # print(user_data)
            if request.POST['password'] == user_data.password:
                request.session['email'] = request.POST['email']
                return render(request, "home.html", {"user_data": user_data})
            else:
                return render(request, "login.html", {"msg": "Password Not Match"})
        except:
            return render(request, "login.html", {"msg": "Email Not exist"})
    else:
        return render(request, "login.html")


def profile(request):
    if request.method == "POST":
        user_data = User.objects.get(emailid=request.session['email'])
        if request.POST['password']:
            if request.POST['password'] == request.POST['cpassword']:
                user_data.firstname = request.POST['firstname']
                user_data.lastname = request.POST['lastname']
                user_data.password = request.POST['password']
                user_data.profilepic = request.FILE['profilepic']
                user_data.save()
            else:
                return render(request, "profile.html", {"user_data": user_data, "msg": "Passsword and COnfirm Passwrod Not match"})
        else:
            user_data.firstname = request.POST['firstname']
            user_data.lastname = request.POST['lastname']
            user_data.profilepic = request.FILES['profilepic']
            user_data.save()
        return render(request, "profile.html", {"user_data": user_data})
    else:
        user_data = User.objects.get(emailid=request.session['email'])
        return render(request, "profile.html", {"user_data": user_data})


def view_product(request):
    product_data = Products.objects.all()
    return render(request, "product.html", {"product_data": product_data})


def add_to_cart(request, pk):
    if request.method == "POST":
        product_dataa = Products.objects.get(id=pk)
        buyer_data = User.objects.get(emailid=request.session['email'])
        Cart.objects.create(
            product_detail=product_dataa,
            buyer_detail=buyer_data
        )
        product_data = Products.objects.all()
        return render(request, "product.html", {"product_data": product_data})
    else:
        product_data = Products.objects.all()
        return render(request, "product.html", {"product_data": product_data})


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html', {'msg': 'Cannot logout without login'})


def cart(request):
    user = User.objects.get(emailid=request.session['email'])
    all_cart = Cart.objects.filter(buyer_detail=user)
    total_cart = 0
    for i in all_cart:
        total_cart = total_cart+i.product_detail.product_price
    return render(request, "cart.html", {"all_cart": all_cart, "total": total_cart})

def addform(request):
     if request.method=="POST":
          pass
     else:
          return render(request,"form.html")