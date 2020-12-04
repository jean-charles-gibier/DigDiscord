"""
getsrvmsg
Commande de chargement des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses identifiant(s) de channel

"""
from django.core.management.base import BaseCommand, CommandError
from api.core import base_utils as bu, crawler as cr


class Command(BaseCommand):
    help = 'Loads specified server messages'

    def add_arguments(self, parser):
        parser.add_argument('id_channels', nargs='+', type=int)

    def handle(self, *args, **options):
        discord_token = bu.Configuration.get_from_env('DISCORD_USER_TOKEN', 'NONE')
        base_end_point = bu.Configuration.get_from_env('BASE_END_POINT', 'NONE')
        self.stdout.write(self.style.SUCCESS('Get discord token : "%s"' % discord_token))
        self.stdout.write(self.style.SUCCESS('Get discord end_point : "%s"' % base_end_point))
        crawler = cr.Crawler(discord_token, base_end_point)

        for channel_id in options['id_channels']:
            try:
                crawler.fetch(channel_id, 100)
            except Exception:
                raise CommandError('Channel id "%s" does not exist' % channel_id)

            self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % channel_id))
