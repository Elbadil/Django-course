from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('room/<str:id>/', views.getRoom),
    path('topics/', views.getTopics),
    path('topic/<str:id>/', views.getTopic)
]
