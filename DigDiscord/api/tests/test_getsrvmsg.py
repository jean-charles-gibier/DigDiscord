"""
Test des commandes d'administration custom
"""
from django.core.management import call_command
from django.test import TestCase
from unittest import skipIf
from api.core.base_utils import Configuration
import os


class CommandsTestCase(TestCase):
    def setUp(self):
        """ nothing at the moment """
        pass

    @skipIf(
        os.getenv('DJANGO_SETTINGS_MODULE') == 'DigDiscord.settings.deploy_ci',
        reason="requires secret token")
    def test_getsrvmsg_start(self):
        """ test if manage command getsrvmsg is responding """
        kwargs = {
            "id_channels": ["764519455984058398"],
            "limit": 10,
        }

        if Configuration.findenv("GUILD_ID", "") == 'ID_FROM_CONSTANT':
            print("Some variables are not set (ie :GUILD_ID) this test is avoided !")
            return 0

        call_command("getsrvmsg", **kwargs)
        # TODO verify that we get a json file with 10 elements

        self.assertGreaterEqual(10, 10)

    @skipIf(
        os.getenv('DJANGO_SETTINGS_MODULE') == 'DigDiscord.settings.deploy_ci',
        reason="requires secret token")
    def test_getsrvmsg_all_channels(self):
        """ test all channels option """
        kwargs = {
            "all_channels": True,
            "limit": 10,
        }

        if Configuration.findenv("GUILD_ID", "") == 'ID_FROM_CONSTANT':
            print("Some variables are not set (ie :GUILD_ID) this test is avoided !")
            return 0

        call_command("getsrvmsg", **kwargs)
        # TODO verify that we get a json file with 10 elements

        self.assertGreaterEqual(10, 10)
