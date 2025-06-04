from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import  AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from datetime import timedelta

from .managers import MyUserManager

class MyUser(AbstractBaseUser,PermissionsMixin):
    phone_number =  models.CharField(verbose_name=_('phone number'), max_length=11, unique=True)
    full_name = models.CharField(verbose_name=_('full name'), max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    class Meta:
        verbose_name = _('my users')
        verbose_name_plural = _('my users')

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']

    def get_by_phone(phone):
        try:
            return MyUser.objects.get(phone_number=phone)
        except MyUser.DoesNotExist:
            return None

    def __str__(self):
        return self.full_name


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    date_time_created = models.DateTimeField(auto_now_add=True) 
    expire_time = models.DateTimeField(default=timezone.now() + timedelta(minutes=2))

    class Meta:
        verbose_name = _('otp code')
        verbose_name_plural = _('otp code')

    def __str__(self):
        return f'{self.phone_number}:{self.code}'

    def is_expired(self):
        return timezone.now() > self.expire_time


    

