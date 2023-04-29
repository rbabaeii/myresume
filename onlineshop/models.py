from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid4 , unique= True , editable= False)
    created_at = models.DateTimeField(verbose_name= 'زمان ساخت',auto_now_add=True)
    update_at = models.DateTimeField(verbose_name= 'زمان اپدیت' , auto_now=True)
    class Meta:
        abstract = True


# Products part
User = get_user_model()


class Price(BaseModel):
    price = models.IntegerField(verbose_name='قیمت به ریال' , default=0)

    def __str__(self) -> str:
        return str(self.price)
    
class Product(BaseModel):
    name = models.CharField(verbose_name= 'نام محصول' , max_length=20 )
    description = models.TextField(verbose_name= 'توضیحات محصول' , blank = True)
    price = models.FloatField(verbose_name='قیمت' , default=0 , blank = True)
    finally_price = models.IntegerField(verbose_name='قیمت نهایی' , default= 0 , blank = True , null= True)
    img = models.ImageField(upload_to='static/img/' , verbose_name='عکس' , blank = True)
    quantity = models.IntegerField(default = 1 , verbose_name='تعداد' ,)
    status = models.BooleanField(default=True , verbose_name='وضعیت')
    def __str__(self) -> str:
        return f'{self.name} - {self.finally_price}'
    class Meta:
        ordering = ('-created_at' , )

    def save(self , *args ,**kwargs):
        pricee = Price.objects.all()[0]
        self.finally_price = self.price * pricee.price
        super(Product , self).save()


    

# Order part
class Order(BaseModel):
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name='orders')
    address = models.CharField(verbose_name='آدرس' , max_length=200)
    phone = models.CharField(verbose_name='شماره تلفن' , max_length=11)
    email = models.EmailField(null=True , blank=True)
    total_price = models.PositiveIntegerField(verbose_name='قیمت کل' , null=True , blank=True)
    is_payed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
            return f"{self.phone}-{self.is_payed}"
    
class OrderItem(BaseModel):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='items')
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد' )
    price = models.PositiveIntegerField(verbose_name='قیمت')

    def __str__(self) -> str:
        return f'{self.order.phone}-{self.price}'
    

# contact us model

class ContactUs(BaseModel):
    name = models.CharField(verbose_name='نام' , max_length=20)
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(verbose_name='شماره تلفن' ,blank=True , null=True , max_length=11)
    subject = models.CharField(verbose_name='موضوع' , max_length=50)
    message = models.TextField(verbose_name='پیام')

    def __str__(self) -> str:
        return f"{self.name}-{self.subject}"
    
    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

class Payment(BaseModel):
    # authority = models.CharField( max_length=40)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL ,  null= True  , related_name='payment')
    tracking_code = models.CharField(verbose_name='کد پیگیری' , null=True , unique=True , max_length=10)
    def __str__(self) -> str:
        return f'{self.order.total_price}-{self.tracking_code}'