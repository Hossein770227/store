from django.shortcuts import render

def order_create_view(request):
    return render(request, 'order/order_create.html')
