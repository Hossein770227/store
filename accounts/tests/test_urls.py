from django.test import TestCase
from django.urls import reverse, resolve

from accounts.views import UserRegisterView, UserRegisterCodeView, login_view, logout_view, password_change_view



class AccountsUrlsTest(TestCase):

    def test_user_register_view(self):
        url = reverse('accounts:user_register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)
    
    def test_user_register_code_view(self):
        url= reverse('accounts:verify_code')
        self.assertEqual(resolve(url).func.view_class,UserRegisterCodeView )

    def test_login_view(self):
        url= reverse('accounts:login')
        self.assertEqual(resolve(url).func,login_view )

    def test_logout_view(self):
        url= reverse('accounts:logout')
        self.assertEqual(resolve(url).func,logout_view )

    def test_password_change_view(self):
        url= reverse('accounts:change_password')
        self.assertEqual(resolve(url).func,password_change_view )