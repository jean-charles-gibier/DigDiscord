"""
Test des commandes d'administration custom
"""
from os import environ
from django.test import TestCase
from api.core.crawler import Crawler


class CrawlerCmd(TestCase):
    def setUp(self):
        """
        It's a live test
        if the environnement variables for crawling are not set
        (especially the token value) we can't continue nominal testing
        so we set fake values wich will return, at least, an obvious error.
        """
        print("testing CrawlerCmd")
        if environ.get("GUILD_ID") is None:
            environ["GUILD_ID"] = "ID_FROM_CONSTANT"
        if environ.get("DISCORD_USER_TOKEN") is None:
            environ["DISCORD_USER_TOKEN"] = "DUMMY_TOKEN"
        if environ.get("PATH_STORAGE") is None:
            environ["PATH_STORAGE"] = "/tmp"

    """
    TODO mettre les fausses valeurs dans des fichiers ressources
    """

    def test_fetch_value(self):
        """
        On simule une réponse de l'API
        """
        crawler = Crawler()
        assert crawler is not None
        crawler._token = "DUMMY_TOKEN"
        crawler.fetch_messages("")
        crawler.fetch_messages("", complete_type="older")
        crawler.fetch_messages("", complete_type="newer")
        try:
            crawler.get_channels("GUILD_ID_FOR_TEST")
        except Exception:
            print("Channel not found")
        try:
            crawler.get_channels("GUILD_ID_FOR_TEST", store_it=True)
        except Exception:
            print("Channel not found")
        crawler.get_server()
        crawler.store_server()
        crawler.store_messages()
        crawler._store_channels()
