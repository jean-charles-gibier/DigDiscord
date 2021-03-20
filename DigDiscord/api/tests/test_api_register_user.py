"""
Teste la creation du user customisé
et la restitution du token
"""
# from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
# from rest_framework.authtoken.models import Token
from profileapp.models import CustomUser as cu
from profileapp.models import Profile
from api.views import ProfileManager
from random import randint

class UserRegister(APITestCase):
    def setUp(self):
        """ fixtures """
        self.inputsnewadmin = {"discord_nickname": "admin", "location": "Paris", "record_date": "2020-02-20",
                       "uzer": {"username": "Laurent", "email": "laurent@free.fr", "first_name": "Laurent",
                                "last_name": "Dupont", "password": "ABCD"}}
        self.inputsnewuser = {"discord_nickname": "pouet", "location": "Paris", "record_date": "2021-01-21",
                       "uzer": {"username": "JCrain", "email": "crain@rain.fr", "first_name": "Juliana",
                                "last_name": "Crain", "password": "1234"}}
        # self.token=None

    def new_register_admin(self):
        user = cu.objects.create(
            username=self.inputsnewadmin['uzer']['username'],
            first_name=self.inputsnewadmin['uzer']['first_name'],
            last_name=self.inputsnewadmin['uzer']['last_name'],
            email=self.inputsnewadmin['uzer']['email'],
            is_superuser=True,
        )

        profile = Profile.objects.create(
              uzer=user,
              discord_nickname=self.inputsnewadmin['discord_nickname'],
              location=self.inputsnewadmin['location'],
              record_date=self.inputsnewadmin['record_date'],
        )
        self.assertIsNotNone(profile)

        # self.token = Token.objects.create(user=user)

        # self.assertIsNotNone(self.token)

    def new_register_user(self):
        """
        Ensure we can create a new  profile object via the API.
        """
        url = reverse('profile_manager')
        # on ne change que l'email

        factory = APIRequestFactory()
        user = cu.objects.get(email=self.inputsnewadmin['uzer']['email'])

        # Make an authenticated request to the view...
        self.inputsnewuser['uzer']['email'] = str(randint(0, 100)) + self.inputsnewuser['uzer']['email']
        request = factory.post(url, self.inputsnewuser, format='json')
        force_authenticate(request, user=user) #,  token=self.token)
        view = ProfileManager.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(Profile.objects.get(pk=2).uzer.first_name, 'Juliana')

    def test_new_register_user_admin(self):
        self.new_register_admin()
        self.new_register_user()