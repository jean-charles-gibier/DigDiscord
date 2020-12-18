from api.models import Channel, Link, Message, ModelReference, Server, User
from api.serializers import (
    ChannelSerializer,
    LinkSerializer,
    MessageSerializer,
    ModelReferenceSerializer,
    ServerSerializer,
    UserSerializer,
)
from rest_framework import viewsets


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ModelReferenceViewSet(viewsets.ModelViewSet):
    queryset = ModelReference.objects.all()
    serializer_class = ModelReferenceSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
