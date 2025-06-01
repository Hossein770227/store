from django.urls import path, re_path
import re

from . import views


app_name = 'store'

regex = re.compile(r'^products/(?P<slug>[-\w]+)/$')

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_list'),
    re_path(r'^product/(?P<slug>[-\w]+)/$', views.product_detail_view, name='product_detail'),
]
