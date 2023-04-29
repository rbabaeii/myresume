from cgitb import text
from unicodedata import name
from django.db import models

# Create your models here.

class Comments(models.Model):
    title = models.CharField('موضوع' , max_length=100)
    name = models.CharField("نام نویسنده" , max_length= 100)
    email = models.EmailField('ایمیل')
    text = models.TextField('پیام' , max_length= 300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.created_at}'