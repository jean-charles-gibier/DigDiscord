from django.test import TestCase
import DigDiscord.asgi as a
import DigDiscord.wsgi as w
import passenger_wsgi as p
import wsgi as x

"""
Test asgi / wsgi server
"""


class WsgiTestCase(TestCase):
    """
    TODO mettre les fausses valeurs dans des fichiers ressources
    """

    def setUp(self):
        print("testing WsgiTestCase")

    def test_check_asgi_application_is_defined(self):
        """ test if application is created """
        print("asgi test")
        self.assertIsNotNone(a.application)

    def test_check_wsgi_application_is_defined(self):
        """ test if application is created """
        print("wsgi test")
        self.assertIsNotNone(w.application)

    def test_check_psgi_application_is_defined(self):
        """ test if application is created """
        print("psgi test")
        self.assertIsNotNone(p.application)

    def test_check_xsgi_application_is_defined(self):
        """ test if application is created """
        print("xsgi test")
        self.assertIsNotNone(x.application)
