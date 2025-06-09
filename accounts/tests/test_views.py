from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm


from accounts.forms import UserRegisterForm, VerifyCodeForm
from accounts.models import MyUser


class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.client =Client()
     
    def test_user_register_GET(self):
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register.html')
        self.assertTrue(response.context['form'], UserRegisterForm)
    
    def test_user_register_POST_valid(self):
        response = self.client.post(reverse("accounts:user_register"), data={'phone':'09211234567','full_name': 'hossein hadi amani', 'password1':'password', 'password2':'password' })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:verify_code'))

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:user_register'),data={'phone':'14528','full_name': 'hossein hadi amani', 'password1':'password', 'password2':'password' })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='phone', errors='یک شماره تلفن همراه معتبر ایرانی وارد کنید.')

class USerRegisterCodeViewTest(TestCase):
    def setUp(self):
        self.client= Client()

    def test_User_register_code_GET(self):
        response = self.client.get(reverse('accounts:verify_code'))
        self.assertEqual(response.status_code,302 )

class LoginViewTest(TestCase):
    def test_login_user_GET(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTrue(response.context['form'], AuthenticationForm)

