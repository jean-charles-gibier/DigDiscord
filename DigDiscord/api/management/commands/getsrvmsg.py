"""
getsrvmsg
Commande de chargement des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses identifiant(s) de channel.
"""
from django.core.management.base import BaseCommand, CommandError
from api.core.base_utils import Configuration
from api.core.crawler  import Crawler


class Command(BaseCommand):
    help = 'Loads specified server messages'

    def add_arguments(self, parser):
        parser.add_argument('--id_channels', nargs='*', type=int)
        parser.add_argument('--limit', nargs='?', type=int)

    def handle(self, *args, **options):
        discord_token = Configuration.findenv('DISCORD_USER_TOKEN', 'NONE')
        base_end_point = Configuration.findenv('BASE_END_POINT', 'NONE')
        crawler = Crawler(discord_token, base_end_point)

        limit = options['limit'] or 100
        for channel_id in options['id_channels']:
            try:
                crawler.fetch(channel_id, limit)
                crawler.persist()
            except Exception:
                raise CommandError('Channel id "%s" does not exist' % channel_id)

            self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % channel_id))
