from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.db.models import Q
from django.views.decorators.http import require_GET

from store.models import Product


from .forms import ContactForm


@login_required()
def contact_us_view(request):
    if request.method=='POST':
        form_message =ContactForm(request.POST)
        if form_message.is_valid():
            user_form =form_message.save(commit=False)
            user_form.user = request.user
            user_form.save()
            messages.success(request, _('your message submit successfully'))
            return redirect('store:product_list')

        else:
            messages.error(request, _('please contain fields correctly')) 
            return redirect('website:contact_us')
    else:
        form_message = ContactForm()
    return render(request, 'website/contact_us.html', {'form':form_message})


@require_GET
def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.prefetch_related('category').filter(
            Q(name__icontains=query) | Q(category__title__icontains=query)
        )
    


    return render(request, 'website/search_results.html', {'results': results, 'query': query})