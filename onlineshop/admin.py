from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'description' , 'price', 'status')
    ordering = ('-created_at' , )

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id' , 'price')

class OrderItem(admin.TabularInline):
    model  = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'phone' , 'is_payed')
    inlines = (OrderItem ,)
    list_filter = ('is_payed' ,)

@admin.register(ContactUs)
class ContactusAdmin(admin.ModelAdmin):
    list_display = ( 'id','name' , 'subject')
    ordering = ('-created_at' ,)

admin.site.register(Payment)