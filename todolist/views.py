from django.shortcuts import redirect, render , resolve_url
from django.views import View
from .models import Data , Categories
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class landing_page(View):
    def get(self , request):
        if request.user.is_authenticated == True:
                
            data = Data.objects.filter(user = request.user)
            Category = Categories.objects.all()
            return render(request , "todolist/index.html" , {"todos": data , "categories" : Category })
        else:
            url = resolve_url('account:message2')
            return redirect(f"{url}?m=برای دسترسی به این صفحه باید ابتدا وارد حساب کاربری خود بشوید . پس از 5 ثانیه به صفحه ورود به حساب منتقل میشوید")
        
    def post(self , request):
        if request.user.is_authenticated == True:
            if "taskAdd" in request.POST:
                description = request.POST['description']
                dueDate = str(request.POST['date'])
                category = request.POST['category_select']
                data = Data(description = description ,dueDate = dueDate , category = Categories.objects.get(name = category) , user = request.user)
                data.save()
                return redirect('todo-list')
            elif "taskDelete" in request.POST:
                for k in request.POST:
                    try:
                        data = Data.objects.get(id = k , user = request.user)
                        data.delete()
                        return redirect("todo-list")
                    except:
                        continue
        else:
            url = resolve_url('account:message2')
            return redirect(f"{url}?m=برای دسترسی به این صفحه باید ابتدا وارد حساب کاربری خود بشوید . پس از 5 ثانیه به صفحه ورود به حساب منتقل میشوید")
        
class Update(View):
    def get(self , request , pk):
        if request.user.is_authenticated == True:
            todos = Data.objects.get( id = pk , user = request.user)
            category = Categories.objects.all()
            return render(request , "todolist/todo.html" , {"todo":todos , 'categories' : category})
        else:
            url = resolve_url('account:message2')
            return redirect(f"{url}?m=برای دسترسی به این صفحه باید ابتدا وارد حساب کاربری خود بشوید . پس از 5 ثانیه به صفحه ورود به حساب منتقل میشوید")
           
    def post(self , request , pk):
        if request.user.is_authenticated ==  True:
            todo = Data.objects.get(id = pk)
            title = request.POST['description']
            if request.POST.get('date') is not "":
                due_date = str(request.POST['date'])
                todo.dueDate = due_date
                
            categories = request.POST['category_select']
            todo.description = title
            todo.category = Categories.objects.get(name = categories)
            todo.save()
            return redirect("todo-list")
        else:
            url = resolve_url('account:message2')
            return redirect(f"{url}?m=برای دسترسی به این صفحه باید ابتدا وارد حساب کاربری خود بشوید . پس از 5 ثانیه به صفحه ورود به حساب منتقل میشوید")
           
