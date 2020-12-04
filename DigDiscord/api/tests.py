"""
Test des commandes d'administration custom
"""
from django.test import TestCase
from django.core.management import call_command

class CommandsTestCase(TestCase):
    def setUp(self):
        """ nothing at the moment """
        pass

    def test_getsrvmsg_start(self):
        """ test if getsrvmsg responds """

        args = ['764519455984058398']
        opts = {}
        call_command('getsrvmsg', *args, **opts)
        self.assertGreaterEqual(10, 10)
