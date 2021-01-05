import pprint

from api.models import Channel, Link, Message, ModelReference, Server, User
from api.serializers import (
    ChannelSerializer,
    ChannelsFrequencySerializer,
    LinkSerializer,
    LinksFrequencySerializer,
    MessageSerializer,
    ModelReferenceSerializer,
    ScoreUserGeneralMessageSerializer,
    ServerSerializer,
    UserSerializer,
)
from django.db.models import Count, Max
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView


class ChannelViewSet(viewsets.ModelViewSet):
    """ viewset for Channel object """

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class LinkViewSet(viewsets.ModelViewSet):
    """ viewset for Link object """

    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """ viewset for Message object """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ModelReferenceViewSet(viewsets.ModelViewSet):
    """ viewset for ModelReference object """

    queryset = ModelReference.objects.all()
    serializer_class = ModelReferenceSerializer


class ServerViewSet(viewsets.ModelViewSet):
    """ viewset for Server object """

    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ viewset for User object """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GenericCounter(APIView):
    """perform an object count on DB
    (over an eval if the type-name passed by url is allowed)"""

    def get(self, request, objectname=None, format=None):
        allowed_objects = [
            *{"Channel", "Link", "Message", "ModelReference", "Server", "User"}
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


class ScoreUserGeneralMessage(viewsets.ReadOnlyModelViewSet):
    """ User list by nb of contribution of all users on all forums """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = (
        Message.objects.values("user_id")
        .annotate(
            count_messages=Count("user_id"),
            channel__name=Max("channel__name"),
            user__name=Max("user__name"),
            channel_id=Max("channel_id"),
        )
        .order_by("-count_messages")
    )
    serializer_class = ScoreUserGeneralMessageSerializer

    def get_object(self):
        pass

    @action(detail=True, methods=["GET"])
    def by_channel(self, request, pk=None):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        try:
            channel = Channel.objects.get(pk=self.kwargs[lookup_url_kwarg])
            queryset = (
                Message.objects.values("user_id")
                .filter(channel=channel)
                .annotate(
                    count_messages=Count("user_id"),
                    channel__name=Max("channel__name"),
                    user__name=Max("user__name"),
                    channel_id=Max("channel_id"),
                )
                .order_by("-count_messages")
            )
            obj = get_list_or_404(queryset)

            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            serializer = self.get_serializer(obj, many=True)
            return Response(serializer.data)

        except Channel.DoesNotExist:
            raise Http404

    @action(detail=True, methods=["GET"])
    def by_user(self, request, pk=None):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        try:
            user = User.objects.get(pk=self.kwargs[lookup_url_kwarg])
            queryset = (
                Message.objects.values("channel_id")
                .filter(user=user)
                .annotate(
                    count_messages=Count("user_id"),
                    channel__name=Max("channel__name"),
                    user__name=Max("user__name"),
                    user_id=Max("user_id"),
                )
                .order_by("-count_messages")
            )
            obj = get_list_or_404(queryset)
            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            serializer = self.get_serializer(obj, many=True)
            return Response(serializer.data)

        except User.DoesNotExist:
            raise Http404


class LinksFrequency(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = (
        Link.objects.values("link_content")
        .annotate(count_links=Count("link_md5"), link_md5=Max("link_md5"))
        .order_by("-count_links")
    )
    serializer_class = LinksFrequencySerializer


class ChannelsFrequency(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = (
        Channel.objects.values("name", "identifier", "message__identifier")
        .annotate(count_messages=Count("message__identifier"))
        .order_by("-count_messages")
    )
    serializer_class = ChannelsFrequencySerializer
