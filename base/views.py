from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id': 1, 'name': 'Lets learn Python!'},
    {'id': 2, 'name': 'Lets learn C++!'},
    {'id': 3, 'name': 'Lets learn JavaScript!'},
]

def home(request):
    """"""
    return render(request, 'base/home.html', {'rooms': rooms})

def room(request, id):
    """"""
    s_room = None
    for room in rooms:
        if str(room['id']) == id:
            s_room = room
    return render(request, 'base/room.html', {'room': s_room})
