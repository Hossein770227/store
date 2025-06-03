from django.shortcuts import render

from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', context={'cart':cart})
