from django.http import HttpResponse
import cv2
from .forms import SignupForm
from .models import Signup
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
import datetime
from django.http import JsonResponse
import random
from django.conf import settings
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from mysite import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User, Signup, log, petty_amount


# relative import of forms
# Create your views here.


def index(request):
    try:
        user = User.objects.get(email=request.session['email'])

        if user.usertype == "user":
            request.session['email'] = user.email
            request.session['fname'] = user.fname
    # request.session['profile_pic']=user.profile_pic.url
            return render(request, 'in.html')
        else:
            request.session['email'] = user.email
            request.session['fname'] = user.fname
            # request.session['profile_pic']=user.profile_pic.url
            return render(request, 'visitor_in.html')
    except:
        return render(request, 'index.html')


def validate_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            user = User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']

            )
            if user.usertype == "user":
                request.session['email'] = user.email
                request.session['fname'] = user.fname
            # request.session['profile_pic']=user.profile_pic.url
                return render(request, 'in.html')
            else:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                # request.session['profile_pic']=user.profile_pic.url
                return render(request, 'visitor_in.html')
        except:
            msg = "Email or Password is Incorrect"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')

# def visitor_login(request):
    # if request.method=="POST":
        # try:
        # user=User.objects.get(
        # email=request.POST['email'],
        # password=request.POST['password']

        # )
        # request.session['email']=user.email
        # request.session['fname']=user.fname
        # request.session['profile_pic']=user.profile_pic.url
        # return render(request,'visitor_in.html')
        # except:
        # msg="Email or Password is correct"
        # return render(request,'visitor_in.html',{'msg':msg})
    # else:
        # return render(request,'login.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        # del request.session['profile_pic']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        try:
            Signup.objects.get(emp_code=request.POST['emp_code'])
            # user_detail=Signup.objects.get(mobile=request.POST['mobile'])
            msg = "Emp Code Already Registered"
            return render(request, 'signup.html', {'msg': msg})
        except:
            Signup.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                emp_code=request.POST['emp_code'],
                reason=request.POST['reason'],
                amount=request.POST['amount'],
            )
            amount_fetch = petty_amount.objects.get()
            final_amount = amount_fetch.amount_present - \
                int(request.POST['amount'])
            amount_fetch.amount_present = final_amount
            amount_fetch.save()
            amount_now = petty_amount.objects.get()
            log.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                emp_code=request.POST['emp_code'],
                reason=request.POST['reason'],
                amount=request.POST['amount'],
                type="Debit",
                petty_amount=amount_now.amount_present
            )
        msg = "Petty Cash Entry Successfully"
        return render(request, 'signup.html', {'msg': msg})

    else:
        msg = ""
        return render(request, 'signup.html', {'msg': msg})


def back(request):
    user = User.objects.get(email=request.session['email'])
    if user.usertype == "user":
        request.session['email'] = user.email
        request.session['fname'] = user.fname
        # request.session['profile_pic']=user.profile_pic.url
        return render(request, 'in.html')
    else:
        request.session['email'] = user.email
        request.session['fname'] = user.fname
        # request.session['profile_pic']=user.profile_pic.url
        return render(request, 'visitor_in.html')
        # except:
        # msg="Email or Password is Incorrect"
        # return render(request,'in.html',{'msg':msg})

    # else:
        # return render(request,'visitor_in.html')
    # return render(request,'in.html')


def change_password(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['cnew_password']:
                user.password = request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg = "New password & Confirm New Password Does Not matched"
                return render(request, 'change_password.html', {'msg': msg})
        else:
            msg = "Old Password does Not Matched"
            return render(request, 'change_password.html', {'msg': msg})

    else:
        return render(request, 'change_password.html')


def new_password(request):
    email = request.POST['email']
    np = request.POST['new_password']
    cnp = request.POST['cnew_password']

    if np == cnp:
        user = User.objects.get(email=email)
        user.password = np
        user.save()
        msg = "Password Updated Successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "New Password & Confirm New Password Does Not Matched"
        return render(request, 'new_password.html', {'email': email, 'msg': msg})


def photo_capture(request):
    return render(request, 'photo_capture.html')


def visitor_view(request):
    log_data = log.objects.all()  # .order_by('-id')[:3]
    return render(request, 'visitor_view.html', {'log_data': log_data})


def log_print(request, pk):
    user_detail = log.objects.get(id=pk)
    return render(request, 'log_print.html', {'user_det': user_detail})


def visitor_exit(request):
    all_user = Signup.objects.filter(current_status="Entry")
    return render(request, 'visitor_exit.html', {'signups': all_user})


def mail(request):
    subject = "Greetings"
    msg = "Congratulations for your success"
    to = "test@gmail.com"
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if (res == 1):
        msg = "Mail Sent Successfuly"
    else:
        msg = "Mail could not sent"
    return HttpResponse(msg)


def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Signup, id=id)

    # pass the object as instance in form
    form = SignupForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+id)

    # add form dictionary to context
    context["form"] = form

    return render(request, "update_view.html", context)


def edit_exit(request, pk):
    if request.method == "POST":
        signups = Signup.objects.filter("current_status" == "Entry")
        msg = "Visitor Exit Successfully"
        return render(request, 'edit_exit.html', {'msg': msg, 'signups': signups})
    else:
        signups = Signup.objects.all()
        msg = "Old Password does Not Matched"
        return render(request, 'edit_exit.html', {'signups': signups})


def exit_user(request, pk):
    all_in_user = Signup.objects.filter(current_status="Entry")
    amount_details = Signup.objects.get(id=pk)
    if int(amount_details.amount) <= 0:
        if request.method == "POST":
            signups = Signup.objects.get(id=pk)
            # print(signups)
            signups.current_status = "Exit"
            signups.made_on = datetime.datetime.now()
            signups.save()
            userlog = Signup.objects.get(id=pk)
            all_user = Signup.objects.filter(current_status="Entry")
            msg = "Exit Successfully"
            return render(request, 'visitor_exit.html', {'msg': msg, 'signups': all_user})
        else:
            return render(request, 'visitor_exit.html', {'signups': all_in_user})
    else:
        return render(request, 'visitor_exit.html', {'signups': all_in_user, "msg": "User have some outstandings"})


def forgot_password(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            otp = random.randint(1000, 9999)
            subject = 'Visitor Details'
            message = 'Hello '+user.fname+', Visitor Details '+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'send_email.html', {'otp': otp, 'email': user.email})
        except:
            # msg="Email Does Not Exists"
            return render(request, 'send_email.html')
    else:
        return render(request, 'send_email.html')


def send_email(request, pk):
    if request.method == "POST":
        signups = Signup.objects.get(id=pk)
        subject = 'Petty Cash Details'
        message = f"First Name :- {signups.fname}\n Last Name :- {signups.lname}\n Emp Code :-{signups.emp_code}\n Email-ID :- {signups.email}\n Reason  :- {signups.reason}\n Amount  :- {signups.amount}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        send_mail(subject, message, email_from, recipient_list)
        msg = "E-Mail Sent Successfully"
        return render(request, 'send_email.html', {'signups': signups, 'msg': msg})
    else:
        signups = Signup.objects.get(id=pk)
        return render(request, 'send_email.html', {'signups': signups})


def visitor_search(request):
    if request.method == "POST":
        try:
            user_detail = Signup.objects.get(emp_code=request.POST['emp_code'])
            # signups=Signup.objects.all()
            return render(request, 'visitor_entry.html', {'user_det': user_detail})
        except:
            msg = "Emp Code not register"
            return render(request, 'visitor_search.html', {'msg': msg})
    else:
        return render(request, 'visitor_search.html')


def visitor_entry(request, pk):
    if request.method == "POST":
        userdetails = Signup.objects.get(id=pk)
        userdetails.current_status = "Entry"
        userdetails.amount = int(userdetails.amount) + \
            int(request.POST['address'])
        userdetails.save()
        amount_fetch = petty_amount.objects.get()
        final_amount = amount_fetch.amount_present-int(request.POST['address'])
        amount_fetch.amount_present = final_amount
        amount_fetch.save()
        userlog = Signup.objects.get(id=pk)
        amount_now = petty_amount.objects.get()
        log.objects.create(
            fname=userlog.fname,
            lname=userlog.lname,
            email=userlog.email,
            emp_code=userlog.emp_code,
            reason=request.POST['purpose'],
            amount=request.POST['address'],
            type="Debit",
            petty_amount=amount_now.amount_present
        )
        user_detail = Signup.objects.get(id=pk)

        msg = "Petty Cash Entry Status changed"
        return render(request, 'visitor_entry.html', {'msg': msg, 'user_det': user_detail})
    else:
        return render(request, 'visitor_entry.html')


def camera(request):
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Visitor")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("visitor", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "visitor_image/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()
    return render(request, 'signup.html')


def visitor_log(request):
    return render(request, 'visitor_log.html')


def add_amount(request):
    if request.method == "POST":
        amount_fetch = petty_amount.objects.get()
        final_amount = amount_fetch.amount_present + \
            int(request.POST['amount_add'])
        amount_fetch.amount_present = final_amount
        amount_fetch.save()
        user = User.objects.get(email=request.session['email'])
        amount_now = petty_amount.objects.get()
        log.objects.create(
            fname=user.fname,
            lname=user.lname,
            email=user.email,
            emp_code=00000,
            reason="Cash added admin",
            amount=request.POST['amount_add'],
            type="Credit",
            petty_amount=amount_now.amount_present
        )
        return render(request, 'add_amount.html')
    else:
        return render(request, 'add_amount.html')


def return_amount(request, pk):
    if request.method == "POST":
        amount_details = Signup.objects.get(id=pk)
        final_amount = int(amount_details.amount) - \
            int(request.POST['amount_add'])
        amount_details.amount = final_amount
        amount_details.save()
        amount_fetch = petty_amount.objects.get()
        final_amount = amount_fetch.amount_present + \
            int(request.POST['amount_add'])
        amount_fetch.amount_present = final_amount
        amount_fetch.save()
        amount_now = petty_amount.objects.get()
        log.objects.create(
            fname=amount_details.fname,
            lname=amount_details.lname,
            email=amount_details.email,
            emp_code=amount_details.emp_code,
            reason="Returned Amount",
            amount=request.POST['amount_add'],
            type="Credit",
            petty_amount=amount_now.amount_present
        )
        all_user = Signup.objects.filter(current_status="Entry")
        return render(request, 'visitor_exit.html', {'signups': all_user})
    else:
        amount_details = Signup.objects.get(id=pk)
        return render(request, 'return_amount_page.html', {'amount_fetch': amount_details})
    # pass


def view_cash(request):
    amount_fetch = petty_amount.objects.get()
    return render(request, 'view_cash.html', {'amount_fetch': amount_fetch})
