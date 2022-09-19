
from django.urls import path
from app_api import views
urlpatterns = [
    path('',views.api,name="api"),
    path('getempl/', views.userList.as_view())
]