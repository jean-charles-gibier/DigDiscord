"""
miscellaneous tools and functionalities
"""
import os
import json
import api.constants
import api.core.factory as acf

import logging as lg
# import sys
from sys import (stdout, path)
logger = lg.getLogger(__name__)


import pprint

class Configuration:
    """
    configuration comes
    in completion of "constant" values
    """

    def __init__(self):
        """ defines config properties"""
        self.values = []

    @classmethod
    def set_logger(cls):
        """set log environement."""
        # Set logging stuff
        fh = lg.StreamHandler(stdout)
        formatter = lg.Formatter('%(asctime)s - %(levelname)s -'
                                 ' %(filename)s - %(funcName)s - %(message)s')
        fh.setFormatter(formatter)
        logger = lg.getLogger()

        logger.addHandler(fh)
        logger.setLevel(lg.DEBUG)


    @classmethod
    def findenv(cls, name: str, value: str = '') -> str:
        """ Find the env value from the env,
        the api config or return the default. """

        return os.getenv(name, getattr(api.constants, name, value))

class Builder:

    def __init__(self):
        self.server = None
        self.channels = None
        pass

    @classmethod
    def get_from_json(cls, classtype : type, json_content : str, **kwargs) -> list:
        """
        Get a list of objects defined by classtype
        based from json definition json_content
        (maybe transfered to factory.py)
        :param classtype:
        :param json_content:
        :return: list of objects (even if there is only one)
        """
        class_name = f"acf.{classtype.__name__}Builder"
        func = getattr(eval(class_name), "factory_method")
        raw_objects = json.loads(json_content)
        if type(raw_objects) is list:
            list_objects = [func(**o, **kwargs) for o in raw_objects]
        else:
            list_objects = [func(**raw_objects, **kwargs)]
        return list_objects

