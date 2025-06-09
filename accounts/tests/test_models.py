from django.test import TestCase

from model_bakery import baker

class MyUserTest(TestCase):
    def test_my_user_str(self):
       MyUser=baker.make('MyUser', full_name='hossein hadi amnai')
       self.assertEqual(str(MyUser),'hossein hadi amnai' )


class OtpCodeTest(TestCase):
    def test_otp_code_str(self):
        OtpCode = baker.make("OtpCode", phone_number='09211234567', code='1234')
        self.assertEqual(str(OtpCode), '09211234567:1234')