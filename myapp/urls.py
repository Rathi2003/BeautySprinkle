from django.urls import path 
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('lipstick',views.lipstick,name='lipstick'),
    path('serum',views.serum,name='serum'),
    path('eye',views.eye,name='eye'),
    path('mascara',views.mascara,name='mascara'),
    path('mois',views.mois,name='mois'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]








