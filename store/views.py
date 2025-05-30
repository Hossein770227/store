from django.shortcuts import render
from django.views.generic import TemplateView


class ProductList(TemplateView):
    template_name= 'store/product_list.html'
