from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import MyUser
from website.forms import ContactForm

class TestContactUsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(phone_number='09215274489',full_name='hossein amani', password='testpassword')

    def test_contact_us_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('website:contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/contact_us.html')
        self.assertTrue(response.context['form'], ContactForm)

    def test_contact_us_POST_valid(self):
        self.client.force_login(self.user)
        form_data = {
            'email': 'hossein.h.a770227@gmail.com',
            'subject': 'my subject',
            'message': 'my message',
        }
        response = self.client.post(reverse('website:contact_us'), data=form_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, reverse('store:product_list'))

