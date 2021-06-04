from django.test import TestCase, RequestFactory
from profileapp.managers import CustomUserManager
from profileapp.models import Profile as prof, CustomUser as cu
from django.contrib.auth.models import AnonymousUser

# from profileapp.models import Profile
from profileapp.views import update_profile, create_profile
import sys
import pprint


class CustomUser(TestCase):
    """
    To review
    """

    def setUp(self):
        print("testing CustomUser")

    def test_create_user_std(self):
        try:
            user = CustomUserManager().create_user(
                email="email@email.com",
                password="fake_pw",
                first_name="first_name",
                last_name="last_name",
            )
            assert user is not None
        except Exception:
            print(
                "Unexpected error (create_user):", sys.exc_info()[0], sys.exc_info()[1]
            )

    def test_create_super_user_std(self):
        try:
            superuser = CustomUserManager().create_superuser(
                email="email2@email.com",
                password="fake_pw2",
                first_name="first_name2",
                last_name="last_name2",
            )
            assert superuser is not None
        except Exception:
            print(
                "Unexpected error (create_superuser):",
                sys.exc_info()[0],
                sys.exc_info()[1],
            )


class ProfileAppView(TestCase):
    def setUp(self):
        """
        init conditions of profile management
        :return:
        """
        print("testing ProfileAppView")
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
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
            record_date="2021-01-21",
            nb_min_user_messages=1,
            date_debut="2010-01-01",
            date_fin="2021-03-30",
        )

    def test_create_and_update_profile(self):
        """
        test creation and update of profile custom user
        :return:
        """
        from profileapp.models import Profile, CustomUser

        # Create an instance of a GET request.
        request = self.factory.get("/api/create_profile")
        # request.user = AnonymousUser()

        # logged-in user by setting request.user manually.
        request.user = self.user
        request.user.first_name = "first_name"
        request.user.last_name = "last_name"
        request.user.username = "username"
        request.user.email = "email@toto.fr"
        request.user.profile.discord_nickname = "discord_nickname"
        request.user.profile.location = "location"
        request.user.profile.record_date = "2021-01-21"
        request.user.profile.nb_min_user_messages = 1
        request.user.profile.date_debut = "2010-01-01"
        request.user.profile.date_fin = "2021-03-30"

        response = create_profile(request)
        self.assertEqual(response.status_code, 200)  # OK

        request = self.factory.get("/api/create_profile")
        request.user = self.user
        request.user.first_name = "first_name2"
        request.user.last_name = "last_name2"
        request.user.username = "username2"
        request.user.email = "email2@toto.fr"
        request.user.profile.discord_nickname = "discord_nickname2"
        request.user.profile.location = "location2"
        request.user.profile.record_date = "2021-01-22"
        request.user.profile.nb_min_user_messages = 2
        request.user.profile.date_debut = "2010-01-01"
        request.user.profile.date_fin = "2021-03-30"

        response = update_profile(request)
        self.assertEqual(response.status_code, 200)  # OK

        # requests in PUT Version
        requestp = self.factory.post("/api/create_profile")

        # logged-in user by setting request.user manually.
        requestp.method = "PUT"
        requestp.user = self.user
        requestp.nb_min_user_messages = 3

        response = update_profile(requestp)
        self.assertEqual(response.status_code, 200)  # OK
