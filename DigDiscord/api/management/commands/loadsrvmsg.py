"""
loadsrvmsg
Commande de chargement des messages récupérés par getsrvmsg
server / channel / user and messages
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
from api.core.processor import Processor
import sys


class Command(BaseCommand):
    help = 'register loaded data from files to db'

    def add_arguments(self, parser):
        parser.add_argument('--id_channels', nargs='*', type=int)
        parser.add_argument('--overload', action='store_true')
        parser.add_argument('--all_channels', action='store_true')

    def handle(self, *args, **options):
        guild_id = Configuration.findenv('GUILD_ID', 'NONE')
        processor = Processor(guild_id)

        all_channels = options['all_channels']
        channels = options['id_channels']

        if all_channels:
            pass
            # self.load_channel_list(discord_token, guild_id)
            # channels = self.fetch_channel_list(guild_id)

        try:
            processor.load_server()
            # processor.load_channels()
            # processor.load_messages()
            # processor.load_users()
            # link

        except Exception:
            raise CommandError("Cannot load server msg [{}]".format(sys.exc_info()[0]))

        self.stdout.write(self.style.SUCCESS('Successfully load msg of channels'))
