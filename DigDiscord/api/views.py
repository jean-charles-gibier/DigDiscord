"""
digdiscord views stats and so on
take care that there is a notable adherence to mysql grammar
caused by some raw sql commands
"""
# import pdb
# import pprint

from api.models import Channel, Link, Message, ModelReference, Server, User
from api.serializers import (
    ChannelSerializer,
    ChannelsFrequencySerializer,
    DistributionUserMessageSerializer,
    LinkSerializer,
    LinksFrequencySerializer,
    MessageSerializer,
    ModelReferenceSerializer,
    ScoreUserGeneralMessageSerializer,
    ServerSerializer,
    UserSerializer,
    WordBattleSerializer,
    SearchSerializer,
    UserProfileSerializer
)
from django.db.models import Count, Max
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

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

        if objectname is None:
            uc_object = allowed_objects[0]
        else:
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
    """
    User list by nb of contributions of all users on all forums
    ex :
    scores for all user on all channels:
    GET /api/score/
    all channels scores for one given user:
    GET /api/score/334428165546049536/by_user/
    all users scores for one given channel:
    GET /api/score/347061157351260162/by_channel/
    """

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
        Link.objects.values("link_md5")
        .annotate(
            count_links=Count("link_md5"),
            link_content=Max("link_content"),
            links=Max("links"),
        )
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


class DistributionUserMessage(viewsets.ReadOnlyModelViewSet):
    """id de base : id_user
    declinaisons :
    - by_hour
    - by_weekday
    - by_month
    examples :
    """

    slice_translations = {
        "by_hour": "HOUR",
        "by_weekday": "DAYOFWEEK",
        "by_month": "MONTH",
    }

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Message.objects.raw(
        "SELECT identifier, HOUR(date) as aggregate_name, count(identifier) "
        "as count FROM `api_message`  group by HOUR(date) order by 2"
    )
    # print("all => {}".format(queryset.query))
    serializer_class = DistributionUserMessageSerializer

    @action(
        detail=True,
        methods=["GET"],
        url_path="by_user(?:/(?P<time_slice>[a-z_]*))?",
    )
    def by_user(self, request, time_slice=None, pk=None):
        """
        Perform the lookup filtering. all message by_hour
        time_slice can be 'by_hour' 'by_weekday' 'by_month'
        ex :
        GET /api/distribution/371581173916499969/by_user/by_weekday/
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        if time_slice is None or time_slice not in [
            "by_hour",
            "by_weekday",
            "by_month",
        ]:
            time_slice = "by_hour"

        sql_group = self.slice_translations[time_slice]

        try:
            user_id = self.kwargs[lookup_url_kwarg]
            queryset = Message.objects.raw(
                "SELECT identifier, {}(date) as aggregate_name, count(identifier) as count "
                "FROM `api_message` "
                "where user_id = {} group by {}(date) order by 2".format(
                    sql_group, user_id, sql_group
                )
            )
            print(" query :[{}]".format(queryset.query))

            # May raise a permission denied
            self.check_object_permissions(self.request, queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Channel.DoesNotExist:
            raise Http404

    # TODO : unifiy by_user and by_channel actions
    @action(
        detail=True,
        methods=["GET"],
        url_path="by_channel(?:/(?P<time_slice>[a-z_]*))?",
    )
    def by_channel(self, request, time_slice=None, pk=None):
        """
        Perform the lookup filtering. all message by_hour
        time_slice can be 'by_hour' 'by_weekday' 'by_month'
        ex :
        GET /api/distribution/758607543412457472/by_channel/by_weekday/
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        if time_slice is None or time_slice not in [
            "by_hour",
            "by_weekday",
            "by_month",
        ]:
            time_slice = "by_hour"

        sql_group = self.slice_translations[time_slice]

        try:
            user_id = self.kwargs[lookup_url_kwarg]
            queryset = Message.objects.raw(
                "SELECT identifier, {}(date) as aggregate_name, count(identifier) as count "
                "FROM `api_message` "
                "where channel_id = {} group by {}(date) order by 2".format(
                    sql_group, user_id, sql_group
                )
            )

            # May raise a permission denied
            self.check_object_permissions(self.request, queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Channel.DoesNotExist:
            raise Http404


class WordBattle(viewsets.ReadOnlyModelViewSet):
    """perform a score comparizon between 2 words
    or 2 series of words separed by underscores.
     (Underscores will be interpreted as blank space).
    you must pass this two arguments for instance :
      GET /api/wordbattle/react/vueJS/
    """

    serializer_class = WordBattleSerializer
    queryset = Message.objects.raw(
        "select 0 as identifier, 'none' AS word_1, 0 AS result_1, 'none' AS word_2, 0 AS result_2"
    )

    @action(
        detail=False,
        methods=["GET"],
        url_path="(?P<word_1>[ A-Za-z_-]*)/(?P<word_2>[ A-Za-z_-]*)",
    )
    def get(self, request, word_1="react", word_2="Vue JS"):
        """
        Perform battle of words
        ex :
        GET /api/wordbattle/react/vue_JS/
        (Underscores will be interpreted as blank spaces).
        """

        #  de-slugyffy de-underscores and protect url entries
        word_1 = word_1.replace("_", " ")
        word_2 = word_2.replace("_", " ")

        try:
            queryset = Message.objects.raw(
                """
                SELECT
                0 as identifier,
                '{}' AS word_1,
                (SELECT count(*) FROM api_message WHERE MATCH(content) AGAINST ('{}' IN NATURAL LANGUAGE MODE)) AS result_1,
                '{}' AS word_2,
                (SELECT count(*) FROM api_message WHERE MATCH(content) AGAINST ('{}' IN NATURAL LANGUAGE MODE)) AS result_2
                """.format(
                    word_1, word_1, word_2, word_2
                )
            )

            # May raise a permission denied
            self.check_object_permissions(self.request, queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Message.DoesNotExist:
            raise Http404


class Search(viewsets.ReadOnlyModelViewSet):
    """perform a simple full search text
    """
    # from rest_framework import pagination
    # pagination_class = pagination.PageNumberPagination
    serializer_class = SearchSerializer
    queryset = Message.objects.raw(
        "select 0 as identifier, 'none' AS word"
    )

    @action(
        detail=False,
        methods=["GET"],
        url_path="(?P<word>[ A-Za-z_-]*)",
    )
    def get(self, request, word="Vue JS"):

        """
        Perform search of words
        ex :
        GET /api/search/vue_JS/
        (Underscores will be interpreted as blank spaces).
        At the moment limited to 50 rows
        """
        #  de-slugyffy de-underscores and protect url entries
        word = word.replace("_", " ")

        try:

            statement = """
            SELECT identifier, content, date, channel_id, user_id
            FROM api_message WHERE MATCH(content) AGAINST ('{}' IN NATURAL LANGUAGE MODE)
            order by date desc limit 50
            """.format(
                word
            )

            queryset = Message.objects.raw(
                statement
            )

            # pprint.pprint(queryset)
            # May raise a permission denied
            self.check_object_permissions(self.request, queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Message.DoesNotExist:
            raise Http404


class IsAuthentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, You are authenticated !"}
        return Response(content)


class ProfileManager(APIView):

    def get(self, request):
        content = {"message": "Not yet implemented !"}
        return Response(content)

    def put(self, request):
        content = {"message": "Not yet implemented !"}
        return Response(content)

    def post(self, request):
        import sys
        # create client
        print("Receive post request")
        serializer = UserProfileSerializer(data=request.data)
        try:
            print("Test if serializer.is_valid")
            if serializer.is_valid(raise_exception=True):
                if serializer.create(serializer.data) is not None:
                    print("Should be OK")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('Validation error :' + serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exc:
            print("Erreur post profile : [{}] [{}]".format(sys.exc_info()[0], sys.exc_info()[1]))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

