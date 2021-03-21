"""
Test des commandes d'administration custom
"""
from django.test import TestCase
from api.core.crawler import Crawler

class CrawlerCmd(TestCase):

    def setUp(self):
        """ nothing at the moment """
        print("testing CrawlerCmd")

    """
    TODO mettre les fausses valeurs dans des fichiers ressources
    """
    def test_fetch_value(self):
        """
        On simule une réponse de l'API
        """
        crawler = Crawler()
        assert crawler is not None
        crawler._token = 'DUMMY_TOKEN'
        crawler.fetch_messages("")
        crawler.fetch_messages("", complete_type="older")
        crawler.fetch_messages("", complete_type="newer")
        try:
            crawler.get_channels('0')
        except:
            print("Channel not found")
        try:
            crawler.get_channels('0', store_it=True)
        except:
            print("Channel not found")
        crawler.get_server()
        crawler.store_server()
        crawler._store_server()
        crawler.store_messages()
        crawler._store_channels()
