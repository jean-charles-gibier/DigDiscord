from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Loads specified server messages'

    def add_arguments(self, parser):
        parser.add_argument('id_servers', nargs='+', type=int)

    def handle(self, *args, **options):
        for server_id in options['id_servers']:
            try:
                # poll = Poll.objects.get(pk=poll_id)
                pass
            except Exception : # Poll.DoesNotExistr
                raise CommandError('Server id "%s" does not exist' % server_id)

            # poll.opened = False
            # poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % server_id))
