"""
miscellaneous tools and functionalities
"""
# from typing import Any
import os
import api.constants


class Configuration:
    """
    configuration comes
    in completion of "constant" values
    """

    def __init__(self):
        """ defines config properties"""
        self.values = []

    @classmethod
    def findenv(self, name: str, value: str = '') -> str:
        """ Find the env value from the env,
        the api config or return the default. """

        return os.getenv(name, getattr(api.constants, name, value))