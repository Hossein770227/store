from django.shortcuts import render
from django.views.generic import CreateView

from website.models import Contact

class ContactUs(CreateView):
    model = Contact
