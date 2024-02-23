from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """"""
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    """"""
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null for database and blank is when we save a form
    participants = models.ManyToManyField(User,
                                          related_name='participants',
                                          blank=True)
    updated = models.DateTimeField(auto_now=True) # every time we save this module the datetime is updated
    created = models.DateTimeField(auto_now_add=True) # only saves datetime when we create the model

    class Meta:
        """"""
        ordering = ['-updated', '-created'] # adding dash '-' means we want to order the results of the the query
        # in DESC order which means from the last created/updated to the first
        # the Meta class in Django models allows you to
        # customize various aspects of how the model behaves or
        # interacts with the database, such as default ordering,
        # database table name, indexes, etc. In this case, it's
        # being used to specify the default ordering of records.

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    """"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:50]
