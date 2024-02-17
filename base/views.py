from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Lets learn C++!'},
#     {'id': 3, 'name': 'Lets learn JavaScript!'},
# ]

def home(request):
    """"""
    rooms = Room.objects.all()
    return render(request, 'base/home.html', {'rooms': rooms})

def room(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    print(room)
    return render(request, 'base/room.html', {'room': room})
