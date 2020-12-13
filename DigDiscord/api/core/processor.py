from api.core.base_utils import Configuration
from api.core.crawler import Crawler
from api.core.base_utils import Builder
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
        self.local_name = "fetch_{}.json".format(self.guild_id)
        self.full_path = os.path.join(self.local_path, self.local_name)
        self.local_name = "server_{}.json".format(self.guild_id)
        self.server_path = os.path.join(self.local_path, self.local_name)

    def get_channel_list(self, limit):
        """ read channel list of current guild
         from data repository """
        # get from api discord
        self._refresh_channel_list(limit)
        # fetch results on local
        data = json.load(open(self.full_path, ))
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
        """ get all messages from listed channels
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
        instanciation de tout les objets chargés par loadsrvmsg
        :return:
        """
        # fetch our results on local db
        data = (open(self.server_path, )).read()
        server_object = Builder.get_from_json(Server, data)[0]
        server_object.save()
