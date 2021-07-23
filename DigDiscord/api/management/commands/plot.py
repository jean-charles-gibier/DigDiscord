"""
plot
Commande de generation de fichier image
"""

from api.core.base_utils import Configuration
from api.core.processor import Processor
from snapshot.triggers.generic_plotter import Plotter
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "generate image file plot"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--url", help="""Url where to get stats""", default="")
        parser.add_argument("-val", "--value", help="""Value to aggregate""", default="")
        parser.add_argument("-n", "--name", help="""Name of aggregation""", default="")
        parser.add_argument("-t", "--title", help="""Title of document""", default="")
        parser.add_argument("-fi", "--filename", help="""Name of file""")
        parser.add_argument("-y", "--filetype", help="""Type of file""", default="")
        parser.add_argument("-k", "--token", help="""Token user""", default="")
        parser.add_argument("-sd", "--startdate", help="""Change starting date""", default="")
        parser.add_argument("-ed", "--enddate", help="""Change ending date""", default="")

    def handle(self, *args, **options):
        plotter = Plotter(options)
        plotter.draw()
        self.stdout.write(self.style.SUCCESS(f"Image file '{plotter.get_filename}' generated successfully"))
