from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Features, Product


class ProductList(ListView):
    model = Product
    template_name= 'store/product_list.html'
    context_object_name = 'products'


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    features = Features.objects.filter(product=product)
    return render(request, 'store/product_detail.html', context={'product':product,'features':features })
    
# class ProductDetail(DetailView):
#     model = Product
#     template_name= 'store/product_detail.html'
#     context_object_name = 'product'
