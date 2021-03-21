from django.utils import timezone
from django.test import TestCase, RequestFactory
from api.serializers import MessageSerializer
from api.serializers import ServerSerializer
from api.serializers import ChannelSerializer
from api.models import Channel, Link, Message, ModelReference, Server, User as u


class SerializersTest(TestCase):
    def SetUp(self):
        print("testing SerializersTest")


    def test_channel_serializer(self):
        """
        test return channel
        :return:
        """
        # Create an instance of a GET request.
        creationDate = timezone.now()

        self.channel = Channel.objects.create(
            identifier='identifier',
            name='name',
            topic='topic',
            first_id_message=0,
            last_id_message=0,
            server=Server.objects.create(
                identifier='identifier_s',
                name='name_s',
                )
            )

        self.u = u.objects.create(
            identifier='identifier_u',
            name='name_u',
        )
        self.message = Message.objects.create(
            identifier='Identifier',
            date=creationDate,
            user=self.u,
            channel = self.channel
            )
        self.message.references.set('references')

        self.channelSerializer = ChannelSerializer(instance=self.channel)
        self.messageSerializer = MessageSerializer(instance=self.message)
        self.ServerSerializer = ServerSerializer(instance=self.channel.server)
