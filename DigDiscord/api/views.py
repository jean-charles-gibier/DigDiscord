import pprint

from api.models import Channel, Link, Message, ModelReference, Server, User
from api.serializers import (
    ChannelSerializer,
    LinkSerializer,
    MessageSerializer,
    ModelReferenceSerializer,
    ScoreUserGeneralMessageSerializer,
    ServerSerializer,
    UserSerializer,
)
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


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


class GenericCounter(APIView):
    """perform an object count on DB
    (over an eval if the type-name passed by url is allowed)"""

    def get(self, request, objectname=None, format=None):
        allowed_objects = [
            *set(
                [
                    "Channel",
                    "Link",
                    "Message",
                    "ModelReference",
                    "Server",
                    "User",
                ]
            )
        ]
        if objectname is not None:
            uc_object = objectname[0].upper() + objectname[1:]
        if uc_object in allowed_objects:
            key_object = uc_object + "Count"
            content = {
                key_object: eval(uc_object).objects.aggregate(
                    count=Count("pk")
                )
            }
            return Response(content)


class ScoreUserGeneralMessage(viewsets.ModelViewSet):
    """ User list by nb of contribution on all forums """

    queryset = (
        Message.objects.values("user_id", "user__name")
        .annotate(count_messages=Count("user_id"))
        .order_by("-count_messages")
    )
    serializer_class = ScoreUserGeneralMessageSerializer
