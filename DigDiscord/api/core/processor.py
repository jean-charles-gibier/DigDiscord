from api.core.base_utils import Configuration
from api.core.crawler import Crawler
from api.core.base_utils import Builder
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from api.models import Channel, Link, Message, ModelReference, Server, User
import os.path
import json
import pprint

import logging as lg
import sys

logger = lg.getLogger(__name__)


class Processor:
    def __init__(self, guild_id='NONE', discord_token='NONE'):
        self.server_end_point = Configuration.findenv('GUILD_END_POINT', 'NONE')
        self.channel_end_point = Configuration.findenv('CHANNELS_GUILD_END_POINT', 'NONE')
        self.message_end_point = Configuration.findenv('MESSAGES_CHANNEL_END_POINT', 'NONE')
        self.guild_id = Configuration.findenv('GUILD_ID', guild_id)
        self.discord_token = Configuration.findenv('DISCORD_USER_TOKEN', discord_token)
        self.local_path = Configuration.findenv('PATH_STORAGE', 'data')

        self.channels_name = "fetch_{}.json".format(self.guild_id)
        self.channels_path = os.path.join(self.local_path, self.channels_name)
        self.guild_name = "server_{}.json".format(self.guild_id)
        self.guild_path = os.path.join(self.local_path, self.guild_name)

        self.object_server = None
        self.object_channels = []

    def get_channel_list(self, limit):
        """ read channel list of current guild
         from data repository """
        # get from api discord
        self._refresh_channel_list(limit)
        # fetch results on local
        data = json.load(open(self.channels_path, ))
        return [chan["id"] for chan in data]

    def _refresh_channel_list(self, limit):
        """ get all channel infos from current guild id
         and stores it on data repository """
        crawler = Crawler(self.guild_id)

        try:
            crawler.get_channels(self.guild_id, True)
        except Exception:
            raise "Guild id '{}' does not exist [{}]".format(self.guild_id, sys.exc_info()[0])

        # lg.info\
        print('Successfully fetch channel list of guild : "%s"' % self.guild_id)


    def get_messages_from_channels(self, limit, channels):
        """ get all messages and links from listed channels
        and stores it on data repository """
        crawler = Crawler(self.guild_id)

        for channel_id in channels:
            try:
                crawler.fetch_messages(channel_id, limit)
                crawler.store_messages()
            except Exception:
                raise "Channel id '{}' does not exist [{}]".format(channel_id, sys.exc_info()[0])

            # lg.info\
            print('Successfully fetch msg of channel: "%s"' % channel_id)

    def create_server(self):
        """ make a server from loaded infos """
        crawler = Crawler(self.guild_id)
        crawler.get_server()
        crawler.store_server()

    def load_server(self):
        """
        instanciation de l'objet server (aka guild) chargé par loadsrvmsg
        :return:
        """
        # fetch our results on local db
        data = (open(self.guild_path, )).read()
        object_server = Builder.get_from_json(Server, data)[0]
        object_server.save()
        self.object_server = object_server

    def load_channels(self):
        """
        instanciation des objets channel chargés par loadsrvmsg
        :return:
        """
        # fetch our results on local db
        data = (open(self.channels_path, )).read()
        channel_list = Builder.get_from_json(Channel, data)
        for channel in channel_list:
            try:
                channel.save()
                channel.server = self.object_server
                channel.save()
            except IntegrityError:
                # bypass duplicate key
                pass

        self.object_channels = channel_list

    def load_users(self):
        """
        instanciation des objets user chargés par loadsrvmsg
        :return:
        """

        for channel in self.object_channels:
            messages_name = "fetch_{}.json".format(channel.identifier)
            messages_path = os.path.join(self.local_path, messages_name)
            # fetch our results on local db
            data = (open(messages_path, )).read()
            user_list = Builder.get_from_json(User, data)
            for user in user_list:
                try:
                    user.save()
                    user.channels.add(channel)
                    user.save()
                except IntegrityError:
                    # bypass duplicate key
                    pass

    def load_messages(self):
        """
        instanciation des objets message chargés par loadsrvmsg
        :return:
        """

        for channel in self.object_channels:
            messages_name = "fetch_{}.json".format(channel.identifier)
            messages_path = os.path.join(self.local_path, messages_name)
            # fetch our results on local db
            data = (open(messages_path, )).read()
            message_list = Builder.get_from_json(Message, data)
            for message in message_list:
                try:
                    message.save()
                    message.channel = channel
                    message.user = User.objects.get(identifiant=message.author_id)
                    message.save()
                except IntegrityError:
                    # bypass duplicate key
                    pass
                except ValueError:
                    print("Ne peut enregistrer message pour le channel {}".format(channel.identifier))

    def load_links(self):
        """
        instanciation des objets link chargés par loadsrvmsg
        :return:
        """
        for channel in self.object_channels:
            messages_name = "fetch_{}.json".format(channel.identifier)
            messages_path = os.path.join(self.local_path, messages_name)
            # fetch our results on local db
            data = (open(messages_path, )).read()
            link_list = Builder.get_from_json(Link, data)
            for link in [nn for nn in link_list if nn.link_content is not None]:
                try:
                    link.save()
                    link.links.add(Message.objects.get(identifiant=link.message_id))
                    link.save()
                except IntegrityError:
                    link.links.add(Message.objects.get(identifiant=link.message_id))
                    link.save()

    def trunc_all(self):
        """ trunc all model tables in current api """
        Link.objects.all().delete()
        Message.objects.all().delete()
        Channel.objects.all().delete()
        ModelReference.objects.all().delete()
        Server.objects.all().delete()
        User.objects.all().delete()
