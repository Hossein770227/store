import json
from django.http import HttpResponse
import requests


from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from orders.models import Order

def payment_process_view(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, pk = order_id)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payman/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        "merchant_id":settings.ZARINPAL_MERCHANT_ID,
        "amount":rial_total_price, 
        "description": f'#{order.id}: {order.user.full_name} {order.user.phone_number}',
         'callback_url': 'http://127.0.0.1:7000',
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    print('*'*100)
    data = res.json()['data']
    print(data)
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()
    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')