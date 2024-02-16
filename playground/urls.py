from django.urls import path
from . import views


#URLConf
urlpatterns = [
    path('hello/', views.say_hello_http),
    path('hello/html/', views.say_hello_html)
]
