from django.urls import path
from .views import *
app_name = 'account'

urlpatterns = [
    path('' , Account.as_view() , name='account'),
    path('logout/' , LogOut.as_view() , name='logout'),
    path('message/' , ShowMessage.as_view() , name='message'),
    path('Message/' , ShowMessage2.as_view() , name='message2')
]