from django.shortcuts import render
from django.views.generic import ListView

from .models import Product


class ProductList(ListView):
    model = Product
    template_name= 'store/product_list.html'
    context_object_name = 'products'
