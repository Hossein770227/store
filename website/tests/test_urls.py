from django.test import TestCase
from django.urls import resolve, reverse

from website.views import contact_us_view, search

class TestUrls(TestCase):
    def test_contact_us_url(self):
        url = reverse('website:contact_us')
        self.assertEqual(resolve(url).func, contact_us_view)

    def test_search_url(self):
        url = reverse('website:search')
        self.assertEqual(resolve(url).func, search)