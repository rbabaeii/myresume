from django.shortcuts import render , redirect
from django.views import View
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
        data = Comments(title = title ,name =  name , email = email  , text = message)
        data.save()
        return redirect('/')