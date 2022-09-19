from django.urls import path, include
from app_ajax import views
urlpatterns = [
    path('',views.index,name='index'),
    path('createdata/',views.createdata,name='createdata'),
    path('deleterow/',views.deleterow,name="deleterow")
]
