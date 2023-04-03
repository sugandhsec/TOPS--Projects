from django.urls import path
from app_seller import views
urlpatterns = [
    path('seller_index/',views.seller_index,name='seller_index'),
    path('seller_register/',views.seller_register,name='seller_register'),
    path('seller_otp/',views.seller_otp,name='seller_otp'),
    path('seller_login/',views.seller_login,name='seller_login'),
    path('seller_profile/',views.seller_profile,name='seller_profile'),
    path('seller_logout/',views.seller_logout,name='seller_logout'),
    path('seller_add_product/',views.seller_add_product,name='seller_add_product'),

]