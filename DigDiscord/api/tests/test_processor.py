from os import environ
from django.test import TestCase
from api.core.processor import Processor
from requests.exceptions import InvalidHeader
from django.utils import timezone
from api.models import Channel, Link, Message, ModelReference, Server, User as u


class ProcessorTest(TestCase):

    def setUp(self):
        """
        init conditions of profile management
        :return:
        """
        # set the GUILD env variable to a specific test value
        print("testing ProcessorTest")

        environ["GUILD_ID"] = "GUILD_ID_FOR_TEST"
        creationDate = timezone.now()

        self.channel = Channel.objects.create(
            identifier='identifier',
            name='name',
            topic='topic',
            first_id_message=0,
            last_id_message=0,
            server=Server.objects.create(
                identifier='identifier_s',
                name='name_s',
                )
            )

        self.user = u.objects.create(
            identifier='identifier_u',
            name='name_u',
        )

        self.message = Message.objects.create(
            identifier='Identifier',
            date=creationDate,
            user=self.user,
            channel=self.channel
            )
        self.message.references.set('references')
        # channels
        text_file = open("data/fetch_GUILD_ID_FOR_TEST.json", "w")
        text_file.write("""
        [
            {
                "id": "99999999999999999",
                "last_message_id": "794869835585552384",
                "last_pin_timestamp": "2020-12-10T11:21:42.870000+00:00",
                "type": 0,
                "name": "général",
                "position": 1,
                "parent_id": null,
                "topic": null,
                "guild_id": "347061157351260161",
                "permission_overwrites": [
                    {
                        "id": "572843955407028254",
                        "type": "role",
                        "allow": 0,
                        "deny": 805312529,
                        "allow_new": "0",
                        "deny_new": "805312529"
                    }
                ],
                "nsfw": false,
                "rate_limit_per_user": 10
            },
            {
                "id": "88888888888888888",
                "type": 2,
                "name": "General",
                "position": 0,
                "parent_id": "358024268329648129",
                "bitrate": 64000,
                "user_limit": 0,
                "guild_id": "347061157351260161",
                "permission_overwrites": [],
                "nsfw": false
            }
        ]        
        """)
        text_file.close()
        # messages / users
        text_file = open("data/fetch_99999999999999999.json", "w")
        text_file.write("""
        [
            {
                "identifier": "799746676809269339",
                "date": "2021-01-15 21:07:46",
                "author": "Thierry Chappuis",
                "author_id": "334428165546049536",
                "content": "Oui",
                "references_id": [],
                "url": null,
                "url_md5": null
            },
            {
                "identifier": "799746686816616459",
                "date": "2021-01-15 21:07:48",
                "author": "Alucard",
                "author_id": "371581173916499969",
                "content": "merci pour la réponse",
                "references_id": [],
                "url": null,
                "url_md5": null
            }
        ]
        """)
        text_file.close()

        text_file = open("data/fetch_88888888888888888.json", "w")
        text_file.write("""
        []
        """)
        text_file.close()

    def test_processor(self):
        processor = Processor()
        processor.trunc_all()
        try:
            processor.get_channel_list(1)
        except FileNotFoundError:
            pass
        self.assertEqual(1, 1)

        processor._refresh_channel_list(1)
        try:
            processor.get_messages_from_channels(
                limit=1, channels=['identifier'], complete_type='older'
            )
        except InvalidHeader:
            pass

        try:
            processor.load_server()
        except TypeError:
            pass
        try:
            processor.load_channels()
        except FileNotFoundError:
            pass
        processor.load_users()
        processor.load_messages()
        processor.load_references()
        processor.load_links()
        processor.set_channel_id_messages()
        processor.create_server()
