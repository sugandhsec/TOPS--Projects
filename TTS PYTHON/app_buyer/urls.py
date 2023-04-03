from django.urls import path,include
from app_buyer import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('otp/',views.otp,name="otp"),
    path('login/',views.login,name="login"),
    path('profile/',views.profile,name="profile"),
    path('view_products',views.view_product,name="view_products"),
    path('logout',views.logout,name="logout"),
    path('cart',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('add_to_cart/<int:pk>',views.add_to_cart,name="add_to_cart"),
    path('checkout/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('addform/',views.addform,name="addform"),

    
]