from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class Categories(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.name

# Create your models here.
class Data(models.Model):
    id = models.UUIDField(verbose_name='id' , primary_key=True , unique= True , default= uuid4 , editable=None)
    description = models.CharField(max_length= 100)
    dueDate = models.DateField()
    category = models.ForeignKey(Categories , on_delete= models.SET_NULL , null= True)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null= True)
    def __str__(self) -> str:
        return self.description
