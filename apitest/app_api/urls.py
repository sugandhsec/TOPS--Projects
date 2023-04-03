from django.urls import path,include
from app_api import views

urlpatterns = [
    path("",views.index,name="index"),
    path('getemployees/', views.getemployees)
]