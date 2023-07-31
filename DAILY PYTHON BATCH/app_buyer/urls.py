"""
URL configuration for pro_ecom project.

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
from app_buyer import views

urlpatterns = [
   path('', views.index, name='index'),
   path('dataentry', views.dataentry, name='dataentry'),
   path('showdata', views.showdata, name='showdata'),
   path('delete/<int:pk>', views.delete, name='delete'),
   path('update/<int:pk>', views.update, name='update'),
   path('allcountry', views.allcountry, name='allcountry'),
]