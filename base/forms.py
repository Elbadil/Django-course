from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    """"""
    class Meta:
        """Defining the model and fields = all stands for creating a form
        using the metadata from the room class"""
        model = Room
        fields = '__all__'
