from unicodedata import name
from django.http import JsonResponse
from django.shortcuts import render
from app_ajax.models import User

# Create your views here.
def index(request):
    alldata = User.objects.all()

    return render(request,'index.html',{'key':alldata})

def createdata(request):

    User.objects.create(
        name = request.POST['name'],
        email = request.POST['email'],
        mobile = request.POST['mobile']
    )
    alldata = list(User.objects.values())
 
 
    return JsonResponse({'msg':'Created!!','alldata':alldata})

def deleterow(request):
    row = User.objects.get(id=request.POST['id'])
    row.delete()
    alldata = list(User.objects.values())
    return JsonResponse({'msg':'Deleted!!','alldata':alldata})