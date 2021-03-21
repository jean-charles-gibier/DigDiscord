from api.core.factory import Factory, LinkBuilder, MessageBuilder
from django.test import TestCase

import pprint

class FactoryTest(TestCase):

    def setUp(self):
        """ nothing at the moment """
        print("testing FactoryTest")

    def test_translate_kwargs(self):
        """test mix kwargs """
        translation = {
            "id": "identifier",
            "name": "name",
            "topic": "topic",
            "object_server": "server",
        }
        kwargs = {
            "id": "NONE",
            "name": "NONE",
            "topic": "NONE",
            "object_server": "NONE",
            "add": "add",
        }

        translated_args = Factory.translate_kwargs(
            Factory,
            translation=translation,
            args=kwargs
        )
        assert(translated_args is not None)

        translated_args = LinkBuilder.translate_kwargs(
            Factory,
            translation=translation,
            args=kwargs
        )
        assert(translated_args is not None)

        translated_args = MessageBuilder.translate_kwargs(
            Factory,
            translation=translation,
            args=kwargs
        )
        assert(translated_args is not None)
