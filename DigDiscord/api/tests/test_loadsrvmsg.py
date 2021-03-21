"""
Test des commandes d'administration custom
"""
from django.core.management import call_command
from django.test import TransactionTestCase
from unittest import skipIf
from os import getenv

class LoadSrvMsg(TransactionTestCase):

    def setUp(self):
        """ fixtures """
        print("testing LoadSrvMsg")

    @skipIf(
        getenv('DJANGO_SETTINGS_MODULE') == 'DigDiscord.settings.deploy_ci',
        reason="requires secret token")
    def test_loadsrvmsg_stores_in_db(self):
        """
        test if managed cmd loadsrvmsg is responding
        and loads data in db
        Note : the channel id must match with one defined in test_processor
        """

        kwargs = {"id_channels": ["88888888888888888"]}

        call_command("loadsrvmsg", **kwargs)
        # TODO verify that we get a channel object with the associated msg

    @skipIf(
        getenv('DJANGO_SETTINGS_MODULE') == 'DigDiscord.settings.deploy_ci',
        reason="requires secret token")
    def test_loadsrvmsg_all_channels(self):
        """ same test for all channels """

        pass
        # kwargs = {"all_channels": True}
        #       call_command('loadsrvmsg', **kwargs)
        # TODO verify that we get all channels
