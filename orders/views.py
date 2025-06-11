from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from orders.forms import OrderForm
from orders.models import OrderItems

@login_required
def order_create_view(request):
    cart = Cart(request)
    if len(cart)==0:
        messages.warning(request, 'your cart is empty')
        return redirect('store:product_list')
    if request.method=='POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj=order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()
            for item in cart:
                product = item['product_obj']
                OrderItems.objects.create(
                    order = order_obj,
                    product = product,
                    quantity =item['quantity']  ,
                    price = product.main_price
                )
            cart.clear()
            request.session['order_id']= order_obj.id
            return redirect('payment:payment_process')
    else:
        order_form = OrderForm()
    return render(request, 'order/order_create.html',{'form':order_form})
