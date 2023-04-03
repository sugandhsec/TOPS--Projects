from django.urls import path
from seat import views
urlpatterns = [
    path('', views.get_seat_availability, name='get_seat_availability'),
]