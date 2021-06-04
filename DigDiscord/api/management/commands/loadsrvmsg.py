"""
loadsrvmsg
Commande de chargement des messages récupérés par getsrvmsg
server / channel / user and messages
"""
# import sys

from api.core.base_utils import Configuration
from api.core.processor import Processor
from django.core.management.base import BaseCommand

# , CommandError


class Command(BaseCommand):
    help = "register loaded data from files to db"

    def add_arguments(self, parser):
        parser.add_argument("--id_channels", nargs="*", type=int)
        parser.add_argument("--trunc_all", action="store_true")
        parser.add_argument("--all_channels", action="store_true")
        parser.add_argument("--set_last_first_id", action="store_true")

    def handle(self, *args, **options):
        guild_id = Configuration.findenv("GUILD_ID", "NONE")

        if guild_id == "ID_FROM_CONSTANT":
            print("Some variables are not set (ie :GUILD_ID) this test is avoided !")
            return 0
        processor = Processor(guild_id)

        trunc_all = options["trunc_all"]
        set_last_first = options["set_last_first_id"]

        if trunc_all:
            processor.trunc_all()

        if not set_last_first:
            processor.load_server()
            processor.load_channels()
            processor.load_users()
            processor.load_messages()
            processor.load_links()
            processor.load_references()

        processor.set_channel_id_messages()

        self.stdout.write(self.style.SUCCESS("Successfully load msg of channels"))
