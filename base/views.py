from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RoomForm, UserForm, MyUserCreationForm


# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Lets learn C++!'},
#     {'id': 3, 'name': 'Lets learn JavaScript!'},
# ]


def loginPage(request):
    """"""
    if request.user.is_authenticated:
        return redirect('home')
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # 'objects.get' retrieves a single object
            # checks if the user exists
            user = User.objects.get(email=email)
        except:
            # we don't need to pass it in the context dict it is recognized by the app
            messages.error(request, 'Email does not exist')
            return render(request, 'base/login.html', context)

        # validates users credentials if they match we will create a session
        user = authenticate(request, email=email, password=password)
        # if the credentials does not match
        if not user:
            messages.error(request, 'Wrong Password')
        else:
            # elif the authentication was successful we create a session for the user
            login(request, user)
            next_page = request.GET.get('next')
            return redirect(next_page) if next_page else redirect('home')

    return render(request, 'base/login.html', context)


def logoutUser(request):
    """"""
    logout(request)
    return redirect('home')


def registerPage(request):
    """"""
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # user = form.save(commit=False)
            # before saving the user we need to make sure the username
            # the user entered needs to be saved in lowercase in our database
            # because we will do the same when we get the username
            # when the user wants to login in to our app
            # this is a way to handle case sensitive usernames
            # user.username = user.username.lower()
            # user.save() # now we commit the changes to our users table
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'base/signup.html', context)

@login_required(login_url='login')
def updateUser(request):
    """"""
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=user.id)
    context = {
        'form': form,
    }
    return render(request, 'base/update-user.html', context)


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
    rooms_all = Room.objects.all().count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(
        room__topic__name__icontains=q
    )
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'rooms_count': rooms_all,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)


def userProfile(request, id):
    """"""
    user = User.objects.get(id=int(id))
    user_rooms = user.room_set.all()
    user_messages = user.message_set.all()
    rooms_all = Room.objects.all().count()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': user_rooms,
        'room_messages': user_messages,
        'rooms_count': rooms_all,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)


def room(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    # '_set.all()' Gives us the set of all room_messages of this room
    # Message model has a field room which is a Foreign key
    # to the room model
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user) # this is the way to add an object to a ManyToMany field
        return redirect('room', id=room.id)

    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    """"""
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == "POST": # if its a post request
        topic_name = request.POST.get('topic') 
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            topic=topic,
            host=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # request.POST returns the Data submitted as a key-value pair dict
        # <QueryDict: {'csrfmiddlewaretoken':
        # ['X0XdveekWGlEuocVKRu2RBaRJzFwP6dZbvM7BHd2v84fB0MxI8fEglSD1zTbvUz5'],
        # 'host': ['2'],
        # 'topic': ['2'], 'name': ['Adxel'], 'description': ['ffeGGG']}>
        # We can Pass it to the Form Class 'RoomForm' as an argument

        # if form.is_valid(): # and if all the data is valid and respects all the defined types
            # room = form.save(commit=False)
            # room.host = request.user
            # room.save() # we can use the save method on the form and it directly saves
            #the new Instance Created of the room to our database
        return redirect('home')
    context = {
        'form': form,
        'topics': topics,
        'request_type': "Create",
    }
    return render(request, 'base/create-room.html', context)


@login_required(login_url='login')
def updateRoom(request, id):
    """"""
    topics = Topic.objects.all()
    room = Room.objects.get(id=int(id))
    form = RoomForm(instance=room) # when we pass as argument
    # instance to the RoomForm as a key and and the Room instance as a value
    # we reload all the data of the instance and pass it
    # to the values of the form now the form has labels/attributes
    # and the value for each attribute/label reloaded
    if request.user != room.host:
        return HttpResponse('Unauthorized')
    if request.method == 'POST':
        topic_name = request.POST.get('topic') 
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room) # We specify the instance
        # # we want to update to update a Room
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    context = {
        'form': form,
        'topics': topics,
        'request_type': "Update",
        'room': room,
    }
    return render(request, 'base/create-room.html', context)


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


@login_required(login_url='login')
def updateMessage(request, id):
    """"""
    message = Message.objects.get(id=int(id))
    room_id = message.room.id
    if request.user != message.user:
        return HttpResponse('Unauthorized')
    if request.method == 'POST':
        new_body = request.POST.get('body')
        if message.body == new_body:
            # we won't update the message because it is the same as it used to be
            return redirect('room', id=room_id)
        # else we will update the message body with the new one that was entered
        message.body = new_body
        message.edited = True
        message.save()
        return redirect('room', id=room_id)
    return render(request, 'base/message.html', {'message': message})


@login_required(login_url='login')
def deleteMessage(request, id):
    """"""
    message = Message.objects.get(id=int(id))
    room_id = message.room.id
    if request.user != message.user:
        return HttpResponse('Unauthorized')
    if request.method == 'POST': # if the form is submitted
        message.delete()
        return redirect('room', id=room_id)
    return render(request, 'base/delete.html', {'obj': message.body})
