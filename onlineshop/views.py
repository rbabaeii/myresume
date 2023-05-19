from django.shortcuts import render , redirect , HttpResponse , resolve_url
from django.views import View 
from django.shortcuts import get_object_or_404
from django.views.generic import ListView , DetailView
from .models import *
from .utils import Cart , get_payment_gateway , verify_payment  , create_tracking_code
from django.core.paginator import Paginator
# home page view

class HomePage(ListView) :
    queryset = Product.objects.all()
    template_name = 'onlineshop/index.html'


# Products View
class ListProductView(View):
    def get(self , request):
        product = Product.objects.filter(status = True)
        paginator = Paginator(product , 3)
        page_number = request.GET.get('page')
        object_list = paginator.get_page(page_number)
        return render(request  , 'onlineshop/shop.html' , {'object_list':object_list})
    
    
# class UpdateProductPrice(View):
#     def get(self , request):
#         print('ok')

#         price = Price.objects.all()[0]
        
#         Product.objects.all()
#         print('ok')

        return HttpResponse('ok')

class ProductDetail(View):
    
    def get(self,request , pk):
        if request.user.is_authenticated == True:
            product = Product.objects.get(id = pk)
            return render(request , 'onlineshop/single-product.html' , {'object':product} )
        else:
             
             return redirect('account:account')

# Sessions for cart View
 
class CartDetailView(View):
    def get(self , request):
        if request.user.is_authenticated:
            card = Cart(request)
            return render(request , 'onlineshop/cart.html' , {'Cart':card})
        else:
             
             return redirect('account:account')
           
class AddProductView(View):
    def post(self , request , pk):
        if request.user.is_authenticated == True:

            product = get_object_or_404(Product , id = pk)
            quantity = request.POST.get('quantity')
            card = Cart(request)
            card.add(product , quantity)
            return redirect('onlineshop:cart-detail')
        else:
             
             return redirect('account:account')
           
class RemoveProductView(View):
    def get(self , request , pk):
        if request.user.is_authenticated == True:
            cart = Cart(request)
            cart.delete(pk)
            return redirect('onlineshop:cart-detail')
        else:
             
             return redirect('account:account')
           
# Order View

class OrderDetailView(View):
    def get(self, request , pk ):
        if request.user.is_authenticated == True:
            order = get_object_or_404(Order , id=pk)
            return render(request , 'onlineshop/orderdetail.html' , {'order':order})
        else:
             
             return redirect('account:account')


class OrderCreationView(View):
    def get(self , request):
        if request.user.is_authenticated == True:
            cart = Cart(request)
            return render(request , 'onlineshop/checkout.html' , {'cart':cart})
        else:
             
             return redirect('account:account')
           

    def post(self , request):
        if request.user.is_authenticated == True:
            cart = Cart(request)
            total = cart.total()
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            order,created = Order.objects.get_or_create(user = request.user , is_payed = False)
            if created:
                order.address = address 
                order.user = request.user 
                order.email = email 
                order.phone = phone 
                order.total_price = total
                order.save()
            for item in cart:
                OrderItem.objects.create(order = order , product = item['product'] , quantity = item['quantity'] , price = item['total_price'])

            url = resolve_url('onlineshop:order-detail' , pk=order.id)
            cart.remove_cart(request)
            return redirect(url)
        else:
             
             return redirect('account:account')


class PayOrder(View):
    def get(self , request , pk):
        payment = Payment.objects.get(id = pk)
        return render(request ,'onlineshop/show.html' , {'Payment':payment})
    def post(self , request , pk):
        order = get_object_or_404(Order , id = pk)
        if order.is_payed == False :
            tracking_code = create_tracking_code()
            order.is_payed = True
            order.save()
            payment = Payment.objects.create(order = order , tracking_code = tracking_code)
            payment.save()
            return redirect('onlineshop:order-pay' , pk=payment.id)
        else:
            return HttpResponse({"خطا . این سفارش قبلا پرداخت شده است"}) 
           
# Contact Us View

class ContactUsView(View):
    def get(self , request):
        return render(request , 'onlineshop/contact.html')
    def post(self , request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        data = ContactUs.objects.create(name  = name, email =email, phone =phone, subject =subject, message= message)
        data.save()
        url = resolve_url('account:message')
        return redirect(f"{url}?m=پیام شما با موفقیت ارسال شد پس از ۵ ثانیه به صفحه اول منتقل میشوید")
    


# class PayOrder(View):
#     def get(self , request , pk):
#         order = get_object_or_404(Order , id = pk)
#         if order.is_payed == False:
#             response = get_payment_gateway(amount=order.total_price , description='r',user_phone=order.phone)
#             if response.get('Authority') is not None:
#                 payment = Payment.objects.create(order = order , authority = response['Authority'])
#                 link = f'https://sandbox.zarinpal.com/pg/StartPay/{response["Authority"]}'
#                 return redirect(link)
#             else:
#                 return HttpResponse({"خطای غیرمنتظره ای رخ داد لطفا بعدا دوباره تلا ش کنید"})
#         else:
#             return HttpResponse({"خطا . این سفارش قبلا پرداخت شده است"}) 
        
# class VerifyOrder(View):
#     def get(self , request , *args, **kwargs):
#         authority = request.GET.get('Authority', '')
#         Status = request.GET.get('Status', '')
#         payment = get_object_or_404(Payment , authority = authority)
#         if Status == 'OK' and payment:
#             response = verify_payment(authority=authority , amount= payment.order.total_price)
#             if response['Status'] == 100 or response['Status'] == 101:
#                 order = get_object_or_404(Order , id = payment.order.id)
#                 order.is_payed = True 
#                 order.save()
#                 payment.tracking_code = create_tracking_code()
#                 payment.save()
#                 return render(request , 'onlineshop/order.html' , {'payment':payment})
#             else:
#                 return HttpResponse({"پرداخت با خطا مواجه شد اگر از حساب شما مبلغی کم شده به پشتیبانی پیام بدهید"})

#         else:
#             return HttpResponse({"پرداخت با خطا مواجه شد اگر از حساب شما مبلغی کم شده به پشتیبانی پیام بدهید"})
