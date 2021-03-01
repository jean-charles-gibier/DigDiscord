# api/serializers.py

import pprint
import json
import pdb
# User => Uz for api.models/auth.models distinction
# from django.contrib.auth.models import User as Uz
from profileapp.models import CustomUser as cu
from django.contrib.auth.forms import UserCreationForm
from profileapp.models import Profile
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


class DistributionUserMessageSerializer(
    serializers.HyperlinkedModelSerializer
):
    """ serializer for message aggregate distributions """

    identifier = serializers.SerializerMethodField()
    # hour day month etc.
    aggregate_name = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["identifier", "aggregate_name", "count"]

    def get_identifier(self, obj):
        return obj.identifier

    def get_count(self, obj):
        return obj.count

    def get_aggregate_name(self, obj):
        return obj.aggregate_name


class WordBattleSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for word battle
    TODO : use
    from django.template.defaultfilters import slugify
     slugify(u"test")
    """

    identifier = serializers.SerializerMethodField()
    word_1 = serializers.SerializerMethodField()
    result_1 = serializers.SerializerMethodField()
    word_2 = serializers.SerializerMethodField()
    result_2 = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["identifier", "word_1", "result_1", "word_2", "result_2"]

    def get_identifier(self, obj):
        return obj.identifier

    def get_word_1(self, obj):
        return obj.word_1

    def get_result_1(self, obj):
        return obj.result_1

    def get_word_2(self, obj):
        return obj.word_2

    def get_result_2(self, obj):
        return obj.result_2


class SearchSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for search
    """

    identifier = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    channel_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["identifier", "message", "date", "channel_id", "user_id"]

    def get_identifier(self, obj):
        return obj.identifier

    def get_message(self, obj):
        return obj.content

    def get_date(self, obj):
        return obj.date

    def get_channel_id(self, obj):
        return obj.channel_id

    def get_user_id(self, obj):
        return obj.user_id


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = cu
        exclude = ('groups', 'user_permissions',)

    def validate_username(self, data):
        return data

    def validate_email(self, data):
        return data

    def validate_password(self, data):
        return data

    def create(self, profile_data):
        # create user
        user = cu.objects.create(
              username=profile_data['username'],
              first_name=profile_data['first_name'],
              last_name=profile_data['last_name'],
              email=profile_data['email'],
             )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    uzer = CustomUserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ['discord_nickname', 'location', 'record_date', 'uzer']

    def create(self, validated_data):
        # pdb.set_trace()
        profile_data = validated_data.pop('uzer')

        custuzer = CustomUserSerializer(required=True)
        objuzer = custuzer.create(profile_data)

        # create profile
        profile = Profile.objects.create(
              uzer=objuzer,
              discord_nickname= validated_data['discord_nickname'],
              location= validated_data['location'],
              record_date= validated_data['record_date'],
        )

        return profile
