import email
from random import randrange
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from app_buyer.models import Cart, User
from app_seller.models import Product

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def index(request):
    try:
        user_data = User.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'user_data': user_data})
    except:
        return render(request, 'index.html', {'msg': 'Coming without yuser data'})


def register(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'msg': 'Email Already Exist'})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global temp
                temp = {
                    'fullname': request.POST['fullname'],
                    'email': request.POST['email'],
                    'mobile': request.POST['mobile'],
                    'password': request.POST['password']
                }
                global otp
                otp = randrange(1000, 9999)
                subject = 'OTP FOR REGISTRATION'
                message = f'Hii welcome To My website Your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html', {'msg': 'Password And Confirm Password Not Match'})
    else:
        return render(request, 'register.html')


def otp(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == otp:
            User.objects.create(
                fullname=temp['fullname'],
                email=temp['email'],
                mobile=temp['mobile'],
                password=temp['password']
            )
            return render(request, 'login.html')
        else:
            return render(request, 'otp.html', {'msg': 'OTP IS WRONG '})
    else:
        return render(request, 'register.html')


def login(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'user_data': session_user_data})
    except:
        if request.method == 'POST':
            try:
                session_user = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == session_user.password:
                    request.session['email'] = request.POST['email']
                    cart_obj = Cart.objects.filter(userid=session_user)
                    global order_id
                    if len(cart_obj) != 0:
                        oid = cart_obj.values()
                        order_id = oid[0]['orderid']
                    else:
                        order_id = randrange(1000, 9999)
                    return render(request, 'home.html', {'user_data': session_user, 'msg': 'Welcome To Fruthika'})
                else:
                    return render(request, 'login.html', {'msg': 'Password is Wrong'})
            except:
                return render(request, 'login.html', {'msg': 'Email is Wrong'})
        else:
            return render(request, 'login.html')


def profile(request):
    session_user_data = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        if request.FILES:
            session_user_data.fullname = request.POST['fullname']
            session_user_data.mobile = request.POST['mobile']
            session_user_data.password = request.POST['password']
            session_user_data.pic = request.FILES['pic']
            session_user_data.save()
            return render(request, "profile.html", {'user_data': session_user_data, 'msg': 'Updated Profile Successfully'})
        else:
            session_user_data.fullname = request.POST['fullname']
            session_user_data.mobile = request.POST['mobile']
            session_user_data.password = request.POST['password']
            session_user_data.save()
            return render(request, "profile.html", {'user_data': session_user_data, 'msg': 'Updated Profile Successfully'})
    return render(request, "profile.html", {'user_data': session_user_data})


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, "login.html", {'msg': 'Logged Out Sucessfully'})
    except:
        return render(request, "login.html", {'msg': 'Can\'t LogOut Without Login'})


def products(request):
    session_user_data = User.objects.get(email=request.session['email'])
    products_data = Product.objects.all()
    return render(request, 'products.html', {'products_data_in_html': products_data, 'user_data': session_user_data})


def product_detail(request, pk):
    session_user_data = User.objects.get(email=request.session['email'])
    products_data = Product.objects.get(id=pk)
    return render(request, 'products_detail.html', {'products_data_in_html': products_data, 'user_data': session_user_data})


def add_to_cart(request, pk):
    session_user_data = User.objects.get(email=request.session['email'])
    # products_data_of = Product.objects.all()
    products_data = Product.objects.get(id=pk)
    Cart.objects.create(
        userid=session_user_data,
        prodcutid=products_data,
        orderid=order_id
    )
    return render(request, 'home.html', {'user_data': session_user_data, })


def cart(request):
    session_user_data = User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=session_user_data, orderid=order_id)
    return render(request, "cart.html", {'cart_data': cart_data, 'user_data': session_user_data})


def remove_cart(request, pk):
    prod = Cart.objects.get(id=pk)
    prod.delete()
    session_user_data = User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=session_user_data, orderid=order_id)
    return render(request, "cart.html", {'cart_data': cart_data, 'user_data': session_user_data})


def checkout(request):
    session_user_data = User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=session_user_data)
    cart_data = cart_data.values()
    global single_amount
    single_amount = 0
    for x in cart_data:
        pro_price = Product.objects.get(id=x['prodcutid_id'])
        single_amount += float(pro_price.productprice)
    amount_user_show = single_amount

    currency = 'INR'
    amount = amount_user_show*100  # Rs. 200

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
    context['total_amt'] = amount_user_show
    return render(request, "payment.html", context=context)
# get---1 line---condition---only exact one line----error more than1 or less than 1
# all---all line
# filter---1 se jayda line---condition--more than one line


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
