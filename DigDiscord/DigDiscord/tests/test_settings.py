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
        assert settings.DATABASES is not None
        assert settings.BASE_DIR is not None
        assert settings.ALLOWED_HOSTS is not None
