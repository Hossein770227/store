from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process_view, name='payment_process'),
    path('callback/', views.payment_callback_view, name='payment_call_back'),
]
