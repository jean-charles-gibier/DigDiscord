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
    channel_name = serializers.SerializerMethodField()
    channel_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "user_name",
            "channel_name",
            "identifier",
            "channel_id",
            "count_messages",
        ]

    def get_channel_id(self, obj):
        #        pprint.pprint(obj)
        return obj["channel_id"]

    def get_count_messages(self, obj):
        return obj["count_messages"]

    def get_identifier(self, obj):
        return obj["user_id"]

    def get_user_name(self, obj):
        return obj["user__name"]

    def get_channel_name(self, obj):
        return obj["channel__name"]


class LinksFrequencySerializer(serializers.HyperlinkedModelSerializer):
    """ serializer for frequency list of links"""

    count_links = serializers.SerializerMethodField()
    link_content = serializers.SerializerMethodField()
    link_md5 = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["link_content", "link_md5", "count_links"]

    def get_link_md5(self, obj):
        return obj["link_md5"]

    def get_link_content(self, obj):
        return obj["link_content"]

    def get_count_links(self, obj):
        return obj["count_links"]


class ChannelsFrequencySerializer(serializers.HyperlinkedModelSerializer):
    """ serializer for frequency of channels"""

    count_messages = serializers.SerializerMethodField()
    channel_id = serializers.SerializerMethodField()
    channel_name = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["channel_name", "channel_id", "count_messages"]

    def get_count_messages(self, obj):
        return obj["count_messages"]

    def get_channel_id(self, obj):
        return obj["identifier"]

    def get_channel_name(self, obj):
        return obj["name"]
