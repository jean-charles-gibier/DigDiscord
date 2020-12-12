"""
loadsrvmsg
Commande de chargement des messages récupérés par getsrvmsg
server / channel / user and messages
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
import sys


class Command(BaseCommand):
    help = 'register loaded data from files to db'

    def add_arguments(self, parser):
        parser.add_argument('--id_channels', nargs='*', type=int)
        parser.add_argument('--overload', action='store_true')
        parser.add_argument('--all_channels', action='store_true')

    def handle(self, *args, **options):
        discord_token = Configuration.findenv('DISCORD_USER_TOKEN', 'NONE')
        path = Configuration.findenv('PATH_STORAGE', 'data')
        guild_id = Configuration.findenv('GUILD_ID', 'NONE')

        all_channels = options['all_channels']
        channels = options['id_channels']

        if all_channels:
            self.get_channel_list(discord_token, 0, guild_id)
            channels = self.fetch_channel_list(guild_id)

        self.get_channels_msg(discord_token, 0, channels)
