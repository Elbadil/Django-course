from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm


# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Lets learn C++!'},
#     {'id': 3, 'name': 'Lets learn JavaScript!'},
# ]


def loginPage(request):
    """"""
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            # 'objects.get' retrieves a single object
            # checks if the user exists
            user = User.objects.get(username=username)
        except:
            # we don't need to pass it in the context dict it is recognized by the app
            messages.error(request, 'User does not exist')

        # validates users credentials if they match we will create a session
        user = authenticate(request, username=username, password=password)
        # if the credentials does not match
        if not user:
            messages.error(request, 'Wrong Password')
        else:
            # elif the authentication was successful we create a session for the user
            login(request, user)
            return redirect('home')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    """"""
    logout(request)
    return redirect('home')


def registerPage(request):
    """"""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # before saving the user we need to make sure the username
            # the user entered needs to be saved in lowercase in our database
            # because we will do the same when we get the username
            # when the user wants to login in to our app
            # this is a way to handle case sensitive usernames
            user.username = user.username.lower()
            user.save() # now we commit the changes to our users table
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occurred During Registration')
    context = {
        'page': 'register',
        'form': form
    }
    return render(request, 'base/login_register.html', context)


def home(request):
    """"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # if q is None we will set it to an empty string
    # we use icontains so even for example q != Python but has 'Py'
    # we'll still be able to return the results for Python Rooms
    # But in case the q is set to an empty string icontains
    # returns all the rooms we have in our db
    #'objects.filter' retrieves all the objects where field is equal to value
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | # Topic Name Rooms
        Q(name__icontains=q) | # Room Name
        Q(description__icontains=q) # Room Description
    )
    # We use The Q class so we can be able to add '&' and '|' operators
    # to perform multiple search in the Rooms we have registered
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request, 'base/home.html', context)


def room(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    return render(request, 'base/room.html', {'room': room})


@login_required(login_url='login')
def createRoom(request):
    """"""
    form = RoomForm()
    if request.method == "POST": # if its a post request
        form = RoomForm(request.POST) # request.POST returns the Data submitted as a key-value pair dict
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


@login_required(login_url='login')
def updateRoom(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    form = RoomForm(instance=room) # when we pass as argument
    # instance to the RoomForm as a key and and the Room instance as a value
    # we reload all the data of the instance and pass it
    # to the values of the form now the form has labels/attributes
    # and the value for each attribute/label reloaded
    if request.user != room.host:
        return HttpResponse('Unauthorized')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room) # We specify the instance
        # we want to update to update a Room
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    if request.user != room.host:
        return HttpResponse('Unauthorized')
    if request.method == 'POST': # if the form is submitted
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room.name})
