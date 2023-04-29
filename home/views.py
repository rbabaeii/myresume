from django.shortcuts import render , redirect, resolve_url
from django.views import View
from onlineshop.models import ContactUs
from .models import Comments
# home page view

class Home_page(View):
    def get(self ,request):
        return render(request , "home/index.html")

    def post(self , request):
        title = request.POST['title']
        name =  request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        data = ContactUs(name = name , email = email , subject = title ,  message = message)
        data.save()
        
        url = resolve_url('account:message')
        return redirect(f"{url}?m=پیام شما با موفقیت ارسال شد پس از ۵ ثانیه به صفحه اول منتقل میشوید")