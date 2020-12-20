"""
Test des commandes d'administration custom
"""
from django.core.management import call_command
from django.test import TransactionTestCase


class LoadSrvMsg(TransactionTestCase):
    def setUp(self):
        """ fixtures """

    def test_loadsrvmsg_stores_in_db(self):
        """test if managed cmd loadsrvmsg is responding
        and loads data in db"""

        kwargs = {"id_channels": ["764519455984058398"]}

        call_command("loadsrvmsg", **kwargs)
        # TODO verify that we get a channel object with the associated msg

    def test_loadsrvmsg_all_channels(self):
        """ same test for all channels """

        pass
        # kwargs = {"all_channels": True}
        #       call_command('loadsrvmsg', **kwargs)
        # TODO verify that we get all channels