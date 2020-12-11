"""
getsrvmsg
Commande de récupération des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses id(s) de channel.
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
from api.core.crawler import Crawler
import sys


class Command(BaseCommand):
    help = 'Loads specified (by "--id_channels") server messages (nb limited by "--limit")'

    def add_arguments(self, parser):
        parser.add_argument('--id_channels', nargs='*', type=int)
        parser.add_argument('--limit', nargs='?', type=int)

    def handle(self, *args, **options):
        discord_token = Configuration.findenv('DISCORD_USER_TOKEN', 'NONE')
        channel_end_point = Configuration.findenv('MESSAGES_CHANNEL_END_POINT', 'NONE')

        crawler = Crawler(discord_token)
        crawler.set_end_point(channel_end_point)

        limit = options['limit'] or 100
        for channel_id in options['id_channels']:
            try:
                crawler.fetch_messages(channel_id, limit)
                crawler.persist_messages()
            except Exception:
                raise CommandError("Channel id '{}' does not exist [{}]".format(channel_id , sys.exc_info()[0]))

            self.stdout.write(self.style.SUCCESS('Successfully fetch : "%s"' % channel_id))
