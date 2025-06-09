from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItems

@login_required
def profile_view(request):
    order = Order.objects.filter(user = request.user)
    order_items =OrderItems.objects.filter(order__in = order).all()
    return render(request, 'dashboard/profile.html', {'order_items':order_items, 'orders':order})
