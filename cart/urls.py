from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.cart_detail, name='cart_detail'),
]
