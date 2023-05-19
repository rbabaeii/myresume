
from django.urls import path , include
from .views import landing_page , Update
app_name = 'todo'
urlpatterns = [
    path("" , landing_page.as_view() , name='todo-list' ),
    path('<str:pk>/', Update.as_view() , name='update-todo')
]
