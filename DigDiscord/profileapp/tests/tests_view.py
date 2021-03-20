from django.test import TestCase, RequestFactory
from profileapp.managers import CustomUserManager as cum
from profileapp.models import Profile as prof, CustomUser as cu
from django.contrib.auth.models import AnonymousUser
# from profileapp.models import Profile
from profileapp.views import update_profile, create_profile
import sys

class CustomUser(TestCase):
    """
    To review
    """
    def test_create_user_std(self):
        cm = cum()
        try:
            user = cm.create_user('email@email.com', 'fake_pw')
            assert user != None
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def test_create_super_user_std(self):
        cm = cum()
        try:
            superuser = cm.create_superuser('email@email.com', 'fake_pw')
            assert superuser != None
        except:
            print("Unexpected error:", sys.exc_info()[0])


class ProfileAppView(TestCase):
    def setUp(self):
        """
        init conditions of profile management
        :return:
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = cu.objects.create(
            username='username',
            first_name='first_name',
            last_name='last_name',
            email='email@biz.com',
            is_superuser=True,
        )
        self.prof = prof.objects.create(
            uzer=self.user,
            discord_nickname='discord_nickname',
            location='location',
            record_date='2021-01-21'
        )

    def test_create_and_update_profile(self):
        """
        test creation and update of profile custom user
        :return:
        """
        # Create an instance of a GET request.
        request = self.factory.get('/api/user')
        request.user = AnonymousUser()

        # logged-in user by setting request.user manually.
        request.user = self.user
        request.user.first_name = "first_name"
        request.user.last_name = "last_name"
        request.user.username = 'username'
        request.user.email = 'email@toto.fr'
        request.user.profile.discord_nickname = 'discord_nickname'
        request.user.profile.location = 'location'
        request.user.profile.record_date = '2021-01-21'

        response = create_profile(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.user
        request.user.first_name = "first_name2"
        request.user.last_name = "last_name2"
        request.user.username = 'username2'
        request.user.email = 'email2@toto.fr'
        request.user.profile.discord_nickname = 'discord_nickname2'
        request.user.profile.location = 'location2'
        request.user.profile.record_date = '2021-01-22'

        response = update_profile(request)
        self.assertEqual(response.status_code, 200)

        # requests in POST Version
        # logged-in user by setting request.user manually.
        request.user = self.user
        request.method = 'POST'
        request.user.first_name = "first_name"
        request.user.last_name = "last_name"
        request.user.username = 'username'
        request.user.email = 'email@toto.fr'
        request.user.profile.discord_nickname = 'discord_nickname'
        request.user.profile.location = 'location'
        request.user.profile.record_date = '2021-01-21'

        response = create_profile(request)
        self.assertEqual(response, None)

        request.user = self.user
        request.method = 'POST'
        request.user.first_name = "first_name2"
        request.user.last_name = "last_name2"
        request.user.username = 'username2'
        request.user.email = 'email2@toto.fr'
        request.user.profile.discord_nickname = 'discord_nickname2'
        request.user.profile.location = 'location2'
        request.user.profile.record_date = '2021-01-22'

        response = update_profile(request)
        self.assertEqual(response.status_code, 200)
