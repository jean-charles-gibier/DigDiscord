"""
getsrvmsg
Commande de chargement des messages d'un ou plusieurs forum(s) d'un serveur
identifié(s) par son/ses identifiant(s) de channel

"""
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Loads specified server messages'

    def add_arguments(self, parser):
        parser.add_argument('id_channels', nargs='+', type=int)

    def handle(self, *args, **options):
        for channel_id in options['id_channels']:
            try:
                pass
            except Exception :
                raise CommandError('Channel id "%s" does not exist' % channel_id)

            self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % channel_id))
