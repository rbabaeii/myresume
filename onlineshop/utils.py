
CART_SESSION_ID = 'cart'
from .models import Product
from uuid import UUID
from django.shortcuts import resolve_url

class Cart:
    def __init__(self , request) -> None:
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item['product'] = Product.objects.get(id = item['id'])
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def remove_cart(self , request):
        del request.session[CART_SESSION_ID]
        self.save()

    def add(self , product , quantity):
        id = str(product.id) 
        if id not in self.cart:
            self.cart[id] = {'quantity' : 0 ,'price':str(product.finally_price) , 'id' : id }
        self.cart[id]['quantity'] += int(quantity)
        self.save()

    def total(self):
        cart = self.cart.values()
        total = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return total
    
    def delete(self , id):
        if id in self.cart:
            del(self.cart[id])
            self.save()
            
    def save(self):
        self.session.modified = True


# Payment methods

import requests
from django.conf import settings


    #? sandbox merchant 
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'


def get_payment_gateway(amount, description, user_phone):
    ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    merchant_id = '----'
    url = resolve_url('onlineshop:order-verify')
    print(url)
    data = {
        'Amount': amount, 
        'MerchantID': merchant_id, 
        'Description': 'test',
        'Mobile': user_phone,
        'CallbackURL': 'http://localhost:8000/online-shop/order/verify/'
    }
    r = requests.post(ZP_API_REQUEST, json=data)
    return r.json()



def verify_payment(authority, amount):
    ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    merchant_id = '----'
    data = {
        'MerchantID': merchant_id,
        'Authority': authority,
        'Amount': amount,
    }
    r = requests.post(ZP_API_VERIFY, json=data)
    return r.json()

import random
from .models import Payment
def create_tracking_code():
    while True:
        number = random.randint(1111 , 9999)
        if Payment.objects.filter(tracking_code = number).exists():
            continue
        else:
            return number