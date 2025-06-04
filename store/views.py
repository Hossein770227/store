from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext as _

from store.forms import CommentForm

from .models import Category, Features, Product, Comment


class ProductList(ListView):
    model = Product
    template_name= 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 3


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    features = Features.objects.filter(product=product)
    categories = Category.objects.all()
    comments = product.comments.all()
    if request.method =='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, _('comment successfully created')) 
            return redirect("store:product_detail", slug=product.slug)
        else:
            messages.error(request, _('Unfortunately, there was a problem creating the comment.')) 

    else:
        comment_form = CommentForm()
    return render(request, 'store/product_detail.html', context={
        'product':product,
        'features':features, 
        'categories':categories, 
        'comments':comments, 
        'form' :comment_form
        })
    
