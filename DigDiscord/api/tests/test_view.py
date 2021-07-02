from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from profileapp.models import Profile as prof, CustomUser as cu
from rest_framework.test import force_authenticate
from api.views import (
    GenericCounter,
    ScoreUserGeneralMessage,
    DistributionUserMessage,
    WordBattle,
    Search,
    ProfileManager,
)
from api.models import Channel, Link, Message, ModelReference, Server, User as u


class ApiView(TestCase):
    def setUp(self):
        """
        init conditions of profile management
        :return:
        """
        print("testing ApiView")
        # Every test needs access to the request factory.
        creationDate = timezone.now()
        self.factory = RequestFactory()
        self.APIfactory = APIRequestFactory()
        self.user = cu.objects.create(
            username="username",
            first_name="first_name",
            last_name="last_name",
            email="email@biz.com",
            is_superuser=True,
        )

        self.prof = prof.objects.create(
            uzer=self.user,
            discord_nickname="discord_nickname",
            location="location",
            record_date=creationDate,
        )
        self.channel = Channel.objects.create(
            identifier="identifier",
            name="name",
            topic="topic",
            first_id_message=0,
            last_id_message=0,
            server=Server.objects.create(identifier="identifier_s", name="name_s",),
        )

        self.u = u.objects.create(identifier="identifier_u", name="name_u",)
        self.message = Message.objects.create(
            identifier="Identifier",
            date=creationDate,
            user=self.u,
            channel=self.channel,
        )
        self.message.references.set("references")

    def test_profile_manager(self):
        """
        test return profile
        :return:
        """
        # Create an instance of a GET request.
        request = self.APIfactory.get("/api/profile/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        gc_view = ProfileManager.as_view()
        response = gc_view(request, pk='')
        self.assertEqual(response.status_code, 200)

    def test_generic_counter(self):
        """
        test return of counter objects
        :return:
        """
        # Create an instance of a GET request.
        request = self.APIfactory.get("/api/channel/counter")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        gc_view = GenericCounter.as_view()
        response = gc_view(request)
        self.assertEqual(response.status_code, 200)

        # test on selected object
        request = self.APIfactory.get("/api/channel/counter", objectname="Channel")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        gc_view = GenericCounter.as_view()
        response = gc_view(request, objectname="Channel")
        self.assertEqual(response.status_code, 200)

    def test_score_user_general_message(self):
        """
        test score user service
        TODO : channel non enregistrés => a tester
        :return:
        """
        from rest_framework import routers

        router = routers.DefaultRouter()
        router.register(r"/api/score/", ScoreUserGeneralMessage, basename="scoreusergeneralmessage")

        request = self.APIfactory.get("/api/score/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = ScoreUserGeneralMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get("/api/score/347061157351260162/by_channel/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = ScoreUserGeneralMessage.as_view({"get": "by_channel"})
        response = fetcher(request, pk="347061157351260162")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get("/api/score/identifier/by_channel/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = ScoreUserGeneralMessage.as_view({"get": "by_channel"})
        response = fetcher(request, pk="identifier")
        self.assertEqual(response.status_code, 200)

        request = self.APIfactory.get("/api/score/334428165546049536/by_user/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = ScoreUserGeneralMessage.as_view({"get": "by_user"})
        response = fetcher(request, pk="334428165546049536")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get("/api/score/identifier_u/by_user/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = ScoreUserGeneralMessage.as_view({"get": "by_user"})
        response = fetcher(request, pk="identifier_u")
        self.assertEqual(response.status_code, 200)

    def test_distribution_user_message(self):
        """
        test ditributiion user msg value
        :return:
        """
        from rest_framework import routers

        router = routers.DefaultRouter()
        router.register(r"/api/distribution/", DistributionUserMessage)

        request = self.APIfactory.get(
            "/api/distribution/758607543412457472/by_channel/by_hour/"
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = DistributionUserMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="758607543412457472")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get(
            "/api/distribution/identifier/by_channel/by_hour/"
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = DistributionUserMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="identifier")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get(
            "/api/distribution/371581173916499969/by_user/by_weekday/"
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = DistributionUserMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="371581173916499969")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get(
            "/api/distribution/identifier_u/by_user/by_weekday/"
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = DistributionUserMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="identifier_u")
        self.assertEqual(response.status_code, 404)

        request = self.APIfactory.get(
            "/api/distribution/758607543412457472/by_channel/by_weekday/"
        )
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = DistributionUserMessage.as_view({"get": "retrieve"})
        response = fetcher(request, pk="758607543412457472")
        self.assertEqual(response.status_code, 404)

        router.register(r"/api/wordbattle/", WordBattle)
        request = self.APIfactory.get("/api/wordbattle/react/vueJS/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = WordBattle.as_view({"get": "retrieve"})
        response = fetcher(request, pk="reactJS", word_1="reactJS", word_2="Vue")
        self.assertEqual(response.status_code, 404)

        router.register(r"/api/search/vue_JS/", Search)
        request = self.APIfactory.get("/api/search/vue_JS/")
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        fetcher = Search.as_view({"get": "retrieve"})
        response = fetcher(request, pk="reactJS", url_path="reactJS")
        self.assertEqual(response.status_code, 404)
