from api.core.base_utils import Configuration, Builder
from django.test import TestCase


class BaseUtils(TestCase):
    def setUp(self):
        print("testing BaseUtils")

    def test_findenv_existing_env(self):
        """test if we can access to a common env variable"""
        retValue = Configuration.findenv(name="PWD", value="__DEFAULT__")
        assert retValue != "__DEFAULT__"

    def test_findenv_not_existing_env(self):
        """test if we can't access to a unexistant variable """
        retValue = Configuration.findenv(
            name="X212_UN_TRUC_QUI#NE_PEUT_EXISTER_W56ZC", value="__DEFAULT__"
        )
        assert retValue == "__DEFAULT__"

    def test_buid_builder(self):
        """ constructor """
        b = Builder()
        assert b is not None
