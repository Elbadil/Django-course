from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    """"""
    class Meta:
        """"""
        model = User
        fields = [
            'name',
            'username',
            'email',
            'password1',
            'password2',
            'avatar',
        ]


class RoomForm(ModelForm):
    """"""
    class Meta:
        """Defining the model and fields = all stands for creating a form
        using the metadata from the room class"""
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    """"""
    class Meta:
        """"""
        model = User
        fields = ['username', 'name', 'email', 'bio', 'avatar']
