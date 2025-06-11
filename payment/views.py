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


def payment_callback_view(request):
    payment_authority= request.GET.get('Authority')
    payment_status = request.GET.get('Status')
    order = get_object_or_404(order,zarinpal_authority=payment_authority )

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status =='Ok':
        request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    request_data = {
        "merchant_id":settings.ZARINPAL_MERCHANT_ID,
        "amount":rial_total_price, 
        'authority':payment_authority, 
    }
    url = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'
    res = requests.post(url = url, data=json.dumps(request_data), headers=request_header)
    
    if 'data' in res.json() and 'errors' in res.json()['data'] or len(res.json()['data']['errors']) ==0:
        data = res.json()['data']
        payment_code =data ['code']
        if payment_code == 100:
            order.is_paid =True
            order.ref_id = data['ref_id']
            order.save()
            return HttpResponse('پرداخت با موفقیت انجام شد ')
        if payment_code == 101:
            return HttpResponse('پرداخت با موفقیت انجام شد. ابته این پرداخت از قیل انجام شده است ')
        else:
            error_code = res.json()['errors']['code']
            error_message = res.json()['errors']['message']
            return HttpResponse(f"تراکنش ناموفق بود {error_code} {error_message}")
