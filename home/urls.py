from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('' , views.Home_page.as_view() , name='home_page')
]