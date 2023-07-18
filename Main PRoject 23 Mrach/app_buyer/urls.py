"""
URL configuration for pro_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('show_product/', views.show_product, name='show_product'),
    path('single_product/<int:pk>', views.single_product, name='single_product'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('remove_cart/<int:pk>', views.remove_cart, name='remove_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('search/', views.search, name='search'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('countries/', views.countries, name='countries'),
    path('single/', views.single, name='single'),
    path('con_ser/', views.con_ser, name='con_ser'),
]
