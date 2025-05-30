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

    def __str__(self):
        return self.full_name




    

