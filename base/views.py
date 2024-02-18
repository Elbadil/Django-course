from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


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
    return render(request, 'base/room.html', {'room': room})


def createRoom(request):
    """"""
    form = RoomForm()
    if request.method == "POST": # if its a post request
        form = RoomForm(request.POST) # request.POST returns the Data submited as a key-value pair dict
        # <QueryDict: {'csrfmiddlewaretoken':
        # ['X0XdveekWGlEuocVKRu2RBaRJzFwP6dZbvM7BHd2v84fB0MxI8fEglSD1zTbvUz5'],
        # 'host': ['2'],
        # 'topic': ['2'], 'name': ['Adxel'], 'description': ['ffeGGG']}>
        # We can Pass it to the Form Class 'RoomForm' as an argument
        if form.is_valid(): # and if all the data is valid and respects all the defined types
            form.save() # we can use the save method on the form and it directly saves
            #the new Instance Created of the room to our database
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    form = RoomForm(instance=room) # when we pass as argument
    # instance to the RoomForm as a key and and the Room instance as a value
    # we relaod all the data of the instance and pass it
    # to the values of the form now the form has labels/attributes
    # and the value for each attribute/label reloaded
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # We specify the instance
        # we want to update to update a Room
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    if request.method == 'POST': # if the form is submitted
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room.name})
