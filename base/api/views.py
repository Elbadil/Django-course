from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Topic
from .serializers import RoomSerializer, TopicSerializer


@api_view(['GET'])
def getRoutes(request):
    """"""
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    """"""
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # serializing many objects
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, id):
    """"""
    room = Room.objects.get(id=int(id))
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getTopics(request):
    """"""
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTopic(request, id):
    """"""
    topic = Topic.objects.get(id=int(id))
    serializer = TopicSerializer(topic, many=False)
    return Response(serializer.data)
