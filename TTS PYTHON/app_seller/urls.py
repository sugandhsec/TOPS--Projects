from django.urls import path, include
from app_seller import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('otp/', views.otp, name="otp"),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
]
