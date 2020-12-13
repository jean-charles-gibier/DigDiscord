"""
getsrvmsg
Commande de récupération des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses id(s).
ou  du server
ou channels d'un serveur
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
# from api.core.crawler import Crawler
from api.core.processor import Processor
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
        guild_id = Configuration.findenv('GUILD_ID', 'NONE')
        processor = Processor(guild_id)

        limit = options['limit'] or 100
        all_channels = options['all_channels']

        # si all_channels is True => on récupère la liste des channels du serveur
        try:
            channels = processor.get_channel_list(limit) if all_channels else options['id_channels']
            processor.get_messages_from_channels(limit, channels)
            processor.create_server()

        except Exception:
            raise CommandError("Cannot get server msg [{}]".format(sys.exc_info()[0]))

        self.stdout.write(self.style.SUCCESS('Successfully fetch msg of channel'))

