from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('contact/',views.ContactUs.as_view(), name='contact_us'),
]
