from django.test import TestCase

from accounts.forms import UserCreationForm
from accounts.models import MyUser

class UserCreationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MyUser.objects.create_user(phone_number='09211234567', full_name='hossein hadi amani', password='password' )

    def test_valid_data(self):
        form = UserCreationForm(data={'phone_number':'09211234568', 'full_name':'hossein hadi amani', 'password1':'password' , 'password2':'password'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_phone_number(self):
        form = UserCreationForm(data={'phone_number':'09211234567', 'full_name':'hossein hadi amani', 'password1':'password1234', 'password2':'password1234'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error, 'phone_number')

    def test_unmatched_password(self):
        form = UserCreationForm(data={'phone_number':'09211234598', 'full_name':'hossein hadi amani', 'password1':'password1' , 'password2':'password2'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)