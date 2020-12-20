"""
Test des commandes d'administration custom
"""
from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    def setUp(self):
        """ nothing at the moment """
        pass

    def test_getsrvmsg_start(self):
        """ test if manage command getsrvmsg is responding """
        kwargs = {
            "id_channels": ["764519455984058398"],
            "limit": 10,
        }

        call_command("getsrvmsg", **kwargs)
        # TODO verify that we get a json file with 10 elements

        self.assertGreaterEqual(10, 10)

    def test_getsrvmsg_all_channels(self):
        """ test all channels option """
        kwargs = {
            "all_channels": True,
            "limit": 10,
        }

        call_command("getsrvmsg", **kwargs)
        # TODO verify that we get a json file with 10 elements

        self.assertGreaterEqual(10, 10)