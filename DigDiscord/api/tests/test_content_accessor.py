import pprint

from api.core.content_accessor import ContentAcessor
from api.models import Channel, Message
from django.test import TransactionTestCase


class LoadSrvMsg(TransactionTestCase):
    def setUp(self):
        """ nothing at the moment """
        print("testing LoadSrvMsg")

        """ fixtures """
        self.msg01 = Message.objects.create(
            identifier="1000000000001",
            date="2017-08-19T08:48:09.118000+00:00",
            content="bla bla bla 01",
        )
        self.msg02 = Message.objects.create(
            identifier="1000000000002",
            date="2017-08-19T08:48:09.118000+00:00",
            content="bla bla bla 02",
        )

    def test_first_message_in_db(self):
        """test if we con accessing at first message in db"""
        first_msg = ContentAcessor.get_first_message_id()
        assert self.msg01 != first_msg
        first_msg = ContentAcessor.get_first_message_id(0)
        assert self.msg01 != first_msg

    def test_last_message_in_db(self):
        """test if we con accessing at last message in db"""
        last_msg = ContentAcessor.get_last_message_id()
        assert self.msg02 != last_msg
        last_msg = ContentAcessor.get_last_message_id(0)
        assert self.msg02 != last_msg
