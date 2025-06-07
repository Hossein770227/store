from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('', views.order_create_view, name='order_create'),
]
