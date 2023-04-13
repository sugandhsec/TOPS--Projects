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

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from app_seller import views

urlpatterns = [
    path('', views.seller_index, name="seller_index"),
    path("seller_register/", views.seller_register, name="seller_register"),
    path("seller_login/", views.seller_login, name="seller_login"),
    path("seller_otp/", views.seller_otp, name="seller_otp"),
    path("seller_forgot_password/", views.seller_forgot_password,
         name="seller_forgot_password"),
    path("seller_reset_password/", views.seller_reset_password,
         name="seller_reset_password"),
    path("seller_forgot_otp/", views.seller_forgot_otp, name="seller_forgot_otp"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
