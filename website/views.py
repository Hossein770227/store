from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import ContactForm
from .models import Contact

class ContactUs(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'website/contact_us.html'
    success_url = reverse_lazy('website:contact_us')

    def form_valid(self, form):
        messages.success(self.request, "message submitted successfully!")
        return super().form_valid(form)

