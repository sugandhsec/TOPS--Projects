from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('otp/',views.otp,name='otp'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('products/',views.products,name='products'),
    path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),

]