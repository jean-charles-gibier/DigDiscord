import datetime
from abc import ABC, abstractmethod

import pytz
from api.models import Channel, Link, Message, ModelReference, Server, User
from django.forms.fields import DateTimeField


# import pprint


class Factory(ABC):
    """
    The Creator class declares the factory method that is supposed to return an
    object of each class taht implement creation.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def factory_method(cls):
        """"""
        pass

    def translate_kwargs(self, translation: dict, args: dict) -> dict:
        # get 1 map from 2 with different origins => fusion with key translation
        return dict(
            [
                ((k in translation and (translation.get(k))) or k, v)
                for k, v in args.items()
                if k in translation
            ]
        )


"""
Concrete builders.
"""


class ChannelBuilder(Factory):
    """
    Channel builder
    """

    @classmethod
    def factory_method(cls, **kwargs) -> Channel:
        translation = {
            "id": "identifier",
            "name": "name",
            "topic": "topic",
            "object_server": "server",
        }
        translated_args = cls.translate_kwargs(
            cls, translation=translation, args=kwargs
        )
        return Channel(**translated_args)


class LinkBuilder(Factory):
    """
    Link builder
    """

    @classmethod
    def factory_method(cls, **kwargs) -> Link:
        translation = {
            "url": "link_content",
            "url_md5": "link_md5",
            "identifier": "message_id",
        }
        translated_args = cls.translate_kwargs(
            cls, translation=translation, args=kwargs
        )
        return Link(**translated_args)


class MessageBuilder(Factory):
    """
    transform API response (get messages) to object Message  list
    id json / id models
    work around date must be 'timezoned'
    """

    @classmethod
    def factory_method(cls, **kwargs) -> Message:
        translation = {
            "identifier": "identifier",
            "object_user": "user",
            "object_channel": "channel",
            "date": "date",
            "content": "content",
            "author_id": "author_id",
            "references_id": "references_id",
        }
        translated_args = cls.translate_kwargs(
            cls, translation=translation, args=kwargs
        )
        date = DateTimeField().clean(translated_args["date"])
        tz = pytz.timezone("Europe/Paris")
        date.replace(tzinfo=tz)
        translated_args["date"] = date
        return Message(**translated_args)


class ModelReferenceBuilder(Factory):
    """
    used to identify current version of model
    """

    @classmethod
    def factory_method(cls, **kwargs) -> ModelReference:
        return ModelReference()


class ServerBuilder(Factory):
    """
    Server builder
    """

    @classmethod
    def factory_method(cls, **kwargs) -> Server:
        """
        transform API response (get guild) to object Server
        id json / id models
        """

        translation = {"id": "identifier", "name": "name"}
        translated_args = cls.translate_kwargs(
            cls, translation=translation, args=kwargs
        )
        return Server(**translated_args)


class UserBuilder(Factory):
    """
    User builder
    """

    @classmethod
    def factory_method(cls, **kwargs) -> User:
        translation = {
            "author_id": "identifier",
            "author": "name",
            "object_messages": "messages",
        }
        translated_args = cls.translate_kwargs(
            cls, translation=translation, args=kwargs
        )
        return User(**translated_args)
