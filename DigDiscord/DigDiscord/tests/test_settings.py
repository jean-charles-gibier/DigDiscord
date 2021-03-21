from django.conf import settings
# import DigDiscord.settings.deploy_ci
# import DigDiscord.settings.production
from django.test import TestCase

class TestSettings(TestCase):
    """
    Test des valeurs de config par defaut et speciales
    """
    def setUp(self):
        print("testing TestSettings")

    def test_values(self):
        assert settings.DATABASES != None
        assert settings.BASE_DIR  != None
        assert settings.ALLOWED_HOSTS != None
