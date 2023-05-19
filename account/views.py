from django.shortcuts import render , redirect , HttpResponseRedirect  , resolve_url
from django.views import View 
from django.contrib.auth import authenticate , get_user_model , login , logout
from django.http import HttpResponse 
import time
User = get_user_model()

class ShowMessage(View):
    def get(self , request , *args , **kwargs):
        message = request.GET.get('m')
        return   render(request , 'account/message.html' , {'Message':message})
        time.sleep(5)
        return redirect('home:home_page')
    
class ShowMessage2(View):
    def get(self , request):
        message = request.GET.get('m')
        return render(request , 'account/message2.html' , {'Message':message})
        time.sleep(5)
        return redirect('home:home_page')
    
class Account(View):
    def get(self , request):
        if request.user.is_authenticated == True:
            messagee = resolve_url('account:message')

            return redirect(f"{messagee}?m=شما در حال حاضر لاگین هستید \n پس از ۵ ثانیه به صفحه اول منتقل میشوید")
        else:
            return render(request ,'account/index.html')
    def post(self , request):
        if 'login' in request.POST:
            if ('user' and 'password' in request.POST):
                user = request.POST['user']
                password = request.POST['password']
                u = authenticate(request , username = user , password = password)
                if u:
                    login(request=request , user=u)
                    return redirect('/')
                else:
                    # return HttpResponse({'نام کاربری یا گذرواژه اشتباه میباشد لطفا دوباره اقدام فرمایید'})
                    return render(request , 'account/message2.html' , {'Message':' نام کاربری یا گذرواژه اشتباه میباشد لطفا دوباره اقدام فرمایید'})
            else:

                return render(request , 'account/message2.html' , {'Message':'خطا ! لطفا تمامی فیلدها را پر کنید'})
        elif 'signin' in request.POST:
            if ('user' and 'email' and 'password') in request.POST:
                user = request.POST['user']
                email = request.POST['email']
                password = request.POST['password']
                obj , created = User.objects.get_or_create(username = user)
                if created:
                    obj.username = user
                    obj.set_password(password)
                    obj.email = email
                    obj.save()
                    login(request=request , user= obj)
                    return redirect('/')
                else:
                    return render(request , 'account/message2.html' , {'Message':'یک کاربر با این نام کاربری وجود دارد لطفا با نام کاربری دیگری امتحان کنید'})
            else:
                return render(request , 'account/message2.html' , {'Message':'خطا ! لطفا تمامی فیلدها را پر کنید'})
        else:
            return render(request , 'account/message2.html' , {'Message':'خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید'})
class LogOut(View):
    def get(self , request):
        if request.user.is_authenticated:
            logout(request=request)
            return redirect('account:account')
        