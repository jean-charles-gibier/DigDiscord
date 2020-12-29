"""
give access in elements of current schema
"""
from api.models import Message

# from api.models import Channel, Link, Message, ModelReference, Server, User
from django.db.models import Max, Min

# from api.core.content_accessor import Configuration


class ContentAcessor:
    """
    main accessor
    """

    @classmethod
    def get_last_message_id(self, channel_id=None):
        if channel_id is None:
            message = Message.objects.aggregate(Max("identifier"))
        else:
            message = Message.objects.filter(channel=channel_id).aggregate(
                Max("identifier")
            )["identifier__max"]
        return message

    @classmethod
    def get_first_message_id(self, channel_id=None):
        if channel_id is None:
            message = Message.objects.aggregate(Min("identifier"))
        else:
            message = Message.objects.filter(channel=channel_id).aggregate(
                Min("identifier")
            )["identifier__min"]
        return message
