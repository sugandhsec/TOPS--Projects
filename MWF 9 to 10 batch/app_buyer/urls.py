"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app_buyer import views

urlpatterns = [
    # path('check_session/', views.check_session, name='check_session'),

    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('otp', views.otp, name="otp"),
    path('login', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('fotp/', views.fotp, name="fotp"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('logout/', views.logout, name="logout"),
    path('view_products/', views.view_products, name="view_products"),
    path('search/', views.search, name="search"),
    path('product_description/<int:pk>', views.product_description,
         name="product_description"),
    path('add_to_cart/<int:pk>', views.add_to_cart,
         name="add_to_cart"),
    path('delete_cart/<int:pk>', views.delete_cart,
         name="delete_cart"),
    path('view_cart/', views.view_cart,
         name="view_cart"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('region/', views.region, name='region'),
    path('api/products/', views.productlist.as_view()),


]
