"""
Test des commandes d'administration custom
"""
import json
import sys

from api.core.base_utils import Builder

# , Configuration
from api.core.scrapper import Scrapper

# from django.db import transaction
from api.models import Channel, Message, Server, User
from django.db import IntegrityError
from django.test import TransactionTestCase


class BuilderGenerate(TransactionTestCase):
    def setUp(self):
        self.default_server = None

        self.dummy_server = r"""
        {"approximate_member_count": 956,
         "approximate_presence_count": 169,
         "description": null,
         "discovery_splash": null,
         "emojis": [],
         "features": [],
         "icon": "ce3d9b66900decfef65d44df8a306564",
         "id": "347061157351260161",
         "name": "DA Python",
         "splash": null}
         """

        self.dummy_channels = r"""[
        {
            "id": "347061157351260162",
            "last_message_id": "786624495556755526",
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
            "id": "347061157351260163",
            "type": 2,
            "name": "General",
            "position": 0,
            "parent_id": "358024268329648129",
            "bitrate": 64000,
            "user_limit": 0,
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false
        },
        {
            "id": "347074309287837697",
            "type": 2,
            "name": "Salon 1",
            "position": 1,
            "parent_id": "358024268329648129",
            "bitrate": 64000,
            "user_limit": 6,
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false
        },
        {
            "id": "347074331995537409",
            "type": 2,
            "name": "Salon 2",
            "position": 2,
            "parent_id": "358024268329648129",
            "bitrate": 64000,
            "user_limit": 6,
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false
        },
        {
            "id": "347074358407331840",
            "type": 2,
            "name": "Afk",
            "position": 3,
            "parent_id": "358024268329648129",
            "bitrate": 64000,
            "user_limit": 0,
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false
        },
        {
            "id": "347074846313938944",
            "last_message_id": "781906644111589426",
            "last_pin_timestamp": "2018-06-06T18:05:54.647000+00:00",
            "type": 0,
            "name": "liens-et-snippets-utiles",
            "position": 39,
            "parent_id": "463554635831967745",
            "topic": "pour poster des liens relatifs à notre parcours (pas de liens hors sujets, ils seront modéré)",
            "guild_id": "347061157351260161",
            "permission_overwrites": [
                {
                    "id": "347061157351260161",
                    "type": "role",
                    "allow": 66624,
                    "deny": 805761040,
                    "allow_new": "66624",
                    "deny_new": "805761040"
                },
                {
                    "id": "424508495023439884",
                    "type": "role",
                    "allow": 2048,
                    "deny": 0,
                    "allow_new": "2048",
                    "deny_new": "0"
                }
            ],
            "nsfw": false,
            "rate_limit_per_user": 0
        },
        {
            "id": "347075083342446595",
            "last_message_id": "775683315071057921",
            "type": 0,
            "name": "🎮discussion-gamer🎮",
            "position": 42,
            "parent_id": "573794434601451521",
            "topic": "Pour discuter jeux vidéo",
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false,
            "rate_limit_per_user": 0
        },
        {
            "id": "358023367191822338",
            "last_message_id": "786608013892780032",
            "type": 0,
            "name": "v1-projet-1",
            "position": 6,
            "parent_id": "358024027765211137",
            "topic": null,
            "guild_id": "347061157351260161",
            "permission_overwrites": [],
            "nsfw": false,
            "rate_limit_per_user": 0
        }]
        """

        self.dummy_messages = r"""
        [{
        "id": "786973051191427083",
        "type": 0,
        "content": "⚠️ k8s != docker",
        "channel_id": "555361840591536148",
        "author": {
            "id": "722424288824524953",
            "username": "Sam [alternance][Python][P3]",
            "avatar": null,
            "discriminator": "4800",
            "public_flags": 0
        },
        "attachments": [],
        "embeds": [],
        "mentions": [],
        "mention_roles": [],
        "pinned": false,
        "mention_everyone": false,
        "tts": false,
        "timestamp": "2020-12-11T15:09:56.656000+00:00",
        "edited_timestamp": "2020-12-11T15:11:41.016000+00:00",
        "flags": 0
    },
     {
         "id": "786972790380953631",
         "type": 0,
         "content": "ohhhh merci beaucoup 😍",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T15:08:54.474000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786972529755160607",
         "type": 0,
         "content": "<@501693888206077952> si tu cherches à aller encore plus loin: https://kube.academy/\n\nJ'avais participé à une visio conférence, animé par https://www.linkedin.com/in/ndwinton/",
         "channel_id": "555361840591536148",
         "author": {
             "id": "722424288824524953",
             "username": "Sam [alternance][Python][P3]",
             "avatar": null,
             "discriminator": "4800",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [
             {
                 "type": "article",
                 "url": "https://kube.academy/",
                 "title": "Learn Kubernetes. From Experts. For Free.",
                 "description": "Learn Kubernetes. From Experts. For Free.",
                 "provider": {
                     "name": "KubeAcademy",
                     "url": null
                 },
                 "thumbnail": {
                     "url": "https://kube.academy/wp-content/uploads/og-default.png",
                     "proxy_url": "https://images-ext-2.discordapp.net/external/COfuf76zcU8-v1F8ksq2Zc-tCclK_K70unjc9_X-b2o/https/kube.academy/wp-content/uploads/og-default.png",
                     "width": 1200,
                     "height": 630
                 }
             }
         ],
         "mentions": [
             {
                 "id": "501693888206077952",
                 "username": "Gaëlle",
                 "avatar": "f8a460d36b6c725897e5d5610920df86",
                 "discriminator": "2554",
                 "public_flags": 0
             }
         ],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T15:07:52.336000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
    {
        "id": "786960128771489813",
         "type": 0,
         "content": "ohhhh merci beaucoup 😍",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T15:08:54.474000+00:00",
         "edited_timestamp": null,
         "flags": 0
    },
    {
         "id": "786959925036580954",
         "type": 0,
         "content": "j'adore le y a plus qu'à 😂",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:17:47.137000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959828681097226",
         "type": 0,
         "content": "bah y a plus qu'à faire. 😛",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:17:24.164000+00:00",
         "edited_timestamp": "2020-12-11T14:17:33.213000+00:00",
         "flags": 0
     },
     {
         "id": "786959782040829963",
         "type": 0,
         "content": "oui c'est ce que je souhaite",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:17:13.044000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959687672397825",
         "type": 0,
         "content": "pour faire simple il suffirait d'avoir un hebergeur qui hébergerait les deux serveurs, le front et le back, et seul le front servirait son port vers le monde exterieur",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:16:50.545000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959665023811615",
         "type": 0,
         "content": "mis à part me rendre folle. Mais ça c'est une autre histoire...",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:16:45.145000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959580629696552",
         "type": 0,
         "content": "du coup en même temps que je pose la question je vois de moins en moins l'intêret de docker..",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:16:25.024000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959373117161482",
         "type": 0,
         "content": "dans les grandes lignes l'app que je suis en train de créer serait utilisée sur mobile par des utilisateurs lambda qui s'en servirait pour se connecter à leur compte et consulter leurs informations diverses et des services obtenues via une api (l'app fastapi dont je parlais tout à l'heure)",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:15:35.549000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959270112919572",
         "type": 0,
         "content": "Ce sont des serveurs NodeJs en gros",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:15:10.991000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959126177382411",
         "type": 0,
         "content": "donc une \"app front\" c'est un serveur comme un autre au final.",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:14:36.674000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786959003062239242",
         "type": 0,
         "content": "mais aujourd'hui on voit fleurir des applications qui gèrent en effet la partie frontend (ça reste avant tout des serveurs qui génèrent des fichiers statiques et possèdent aussi un backend)",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:14:07.321000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786958758021562429",
         "type": 0,
         "content": "qu'entend tu par \"app front\" ? Car du frontend c'est avant tout des fichiers statiques",
         "channel_id": "555361840591536148",
         "author": {
             "id": "382938149870895105",
             "username": "MikaelB",
             "avatar": "622ff4608a52960478a0ea2642193e97",
             "discriminator": "2541",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:13:08.899000+00:00",
         "edited_timestamp": null,
         "flags": 0
     },
     {
         "id": "786958743518445588",
         "type": 0,
         "content": "(je crois que je vais rendre folle mon mentor 🤣  avec docker.... )",
         "channel_id": "555361840591536148",
         "author": {
             "id": "501693888206077952",
             "username": "Gaëlle",
             "avatar": "f8a460d36b6c725897e5d5610920df86",
             "discriminator": "2554",
             "public_flags": 0
         },
         "attachments": [],
         "embeds": [],
         "mentions": [],
         "mention_roles": [],
         "pinned": false,
         "mention_everyone": false,
         "tts": false,
         "timestamp": "2020-12-11T14:13:05.441000+00:00",
         "edited_timestamp": null,
         "flags": 0
     }
   ]
   """
 
    @unittest.skipIf(
            os.getenv(name,'DJANGO_SETTINGS_MODULE') == 'DigDiscord.settings.deploy_ci')
    def test_create_server_and_hierarchy(self):
        self._create_server()
        self._create_channel()
        self._create_user_and_message()

    def _create_server(self):
        """ test if valid server object can be created from json infos """
        test_id = "347061157351260161"
        server1 = Builder.get_from_json(Server, self.dummy_server)[0]
        server1.save()
        server2 = Server.objects.get(identifiant=test_id)
        server2.save()
        self.default_server = server1
        self.assertEqual(server1, server2)

    def _create_channel(self):
        """ test if valid channel objects can be created from json infos """
        channels = Builder.get_from_json(
            Channel, self.dummy_channels, object_server=self.default_server
        )
        for channel in channels:
            channel.save()
        self.default_list_channel = channels
        self.assertEqual(len(channels), Channel.objects.all().count())

    def _create_user_and_message(self):
        """ test if message/user objects can be created from json infos """
        # on prend le 1er channel (au hasard)
        current_channel = Channel.objects.all()[0]

        # préfiltrage de données normalement opéré par le crawler
        # dans ce test les data / fixtures doivent etre filtrées séparément
        # A revoir avec un mock opérationel (ça dénote sans doute un pb de conception)
        self.dummy_messages = json.dumps(
            Scrapper.message_filter(json.loads(self.dummy_messages))
        )
        users = Builder.get_from_json(User, self.dummy_messages)
        for user in users:
            try:
                user.save()
                user.channels.add(current_channel)
                user.save()
            except IntegrityError:
                # bypass duplicate key
                pass
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                break

        messages = Builder.get_from_json(
            Message, self.dummy_messages, object_channel=current_channel
        )
        for message in messages:
            message.save()
            message.user = User.objects.get(identifiant=message.author_id)
            message.save()
