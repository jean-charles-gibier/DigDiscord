# api/serializers.py

import pprint

from api.models import Channel, Link, Message, ModelReference, Server, User
from rest_framework import serializers


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ("identifier", "name", "topic", "server")


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ("link_md5", "link_content", "links")


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = (
            "identifier",
            "references",
            "content",
            "date",
            "user",
            "channel",
        )


class ModelReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModelReference
        fields = ("reference", "description")


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ("name", "identifier")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("name", "identifier")


class ScoreUserGeneralMessageSerializer(
    serializers.HyperlinkedModelSerializer
):
    """ serializer for user/message jointure """

    count_messages = serializers.SerializerMethodField()
    identifier = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["user_name", "identifier", "count_messages"]

    def get_count_messages(self, obj):
        return obj["count_messages"]

    def get_identifier(self, obj):
        return obj["user_id"]

    def get_user_name(self, obj):
        return obj["user__name"]
