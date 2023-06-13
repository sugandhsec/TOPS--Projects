from django.urls import path
from app_buyer import views

urlpatterns = [
    path('',  views.index , name='index'),
    path('register/',  views.register , name='register'),
    path('otp/',  views.otp , name='otp'),
    path('login/',  views.login , name='login'),
    path('logout/',  views.logout , name='logout'),
    path('profile/',  views.profile , name='profile'),
    path('update_profile/',  views.update_profile , name='update_profile'),

]