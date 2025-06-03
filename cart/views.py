from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _


from store.models import Product
from .forms import AddToCartProductForm
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', context={'cart':cart})



@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])

    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:cart_detail')

@require_POST
def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, _('All products successfully removed from your cart'))
    else:
        messages.warning(request, _('Your cart is already empty'))

    return redirect('store:product_list')