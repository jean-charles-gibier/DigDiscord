"""
getsrvmsg
Commande de récupération des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses id(s).
ou  du server
ou channels d'un serveur
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
from api.core.crawler import Crawler
import os.path
import json
import sys


class Command(BaseCommand):
    help = 'Loads specified informations from discord server :'
    ' guild (AKA server), channels, members, messages'
    ' "--id_channels" specify from which id channel messages are fetched'
    ' "--all_channels" [flag] get all channels messages (nb limited by --limit option)'
    ' "--limit" limit nb of messages (default 100)'
    ' "--sleep" time to wait in ms between api calls'

    def add_arguments(self, parser):
        parser.add_argument('--id_channels', nargs='*', type=int)
        parser.add_argument('--all_channels', action='store_true')
        parser.add_argument('--limit', nargs='?', type=int)
        parser.add_argument('--sleep', nargs='?', type=int)

    def handle(self, *args, **options):
        discord_token = Configuration.findenv('DISCORD_USER_TOKEN', 'NONE')
        guild_id = Configuration.findenv('GUILD_ID', 'NONE')

        limit = options['limit'] or 100
        all_channels = options['all_channels']
        channels = options['id_channels']

        if all_channels:
            self.get_channel_list(discord_token, limit, guild_id)
            channels = self.fetch_channel_list(guild_id)

        self.get_channels_msg(discord_token, limit, channels)

    def fetch_channel_list(self, guild_id):
        """ read channel list of current guild
         from data repository """
        local_path = Configuration.findenv('PATH_STORAGE', 'data')
        local_name = "fetch_{}.json".format(guild_id)
        full_path = os.path.join(local_path, local_name)
        data = json.load(open(full_path, ))
        return [chan["id"] for chan in data]

    def get_channel_list(self, discord_token, limit, guild_id):
        """ get all channel infos from current guild
         and stores it on data repository """
        channel_end_point = Configuration.findenv('CHANNELS_GUILD_END_POINT', 'NONE')

        crawler = Crawler(discord_token)
        crawler.set_end_point(channel_end_point)

        try:
            crawler.get_channels(guild_id)
            crawler.store_channels()
        except Exception:
            raise CommandError("Guild id '{}' does not exist [{}]".format(guild_id, sys.exc_info()[0]))

        self.stdout.write(self.style.SUCCESS('Successfully fetch channel list of guild : "%s"' % guild_id))

    def get_channels_msg(self, discord_token, limit, channels):
        """ get all messages from listed channels
        and stores it on data repository """
        channel_end_point = Configuration.findenv('MESSAGES_CHANNEL_END_POINT', 'NONE')

        crawler = Crawler(discord_token)
        crawler.set_end_point(channel_end_point)

        for channel_id in channels:
            try:
                crawler.fetch_messages(channel_id, limit)
                crawler.store_messages()
            except Exception:
                raise CommandError("Channel id '{}' does not exist [{}]".format(channel_id, sys.exc_info()[0]))

            self.stdout.write(self.style.SUCCESS('Successfully fetch msg of channel: "%s"' % channel_id))
