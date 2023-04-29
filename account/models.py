from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    address = models.CharField(verbose_name='آدرس' , max_length=200 , null=True , blank=True , default='re')
    postal_code = models.CharField(verbose_name='کد پستی' , max_length=20 , null=True , blank=True , default='s')
