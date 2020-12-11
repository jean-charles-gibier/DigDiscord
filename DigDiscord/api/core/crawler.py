"""
Le crawler récupere l'info brute
(tandis que le scrapper lui donne une
consistance en parsant le resulat du crawler)
"""

from time import sleep
import requests
import sys
import json
import os.path
from .scrapper import Scrapper
from .base_utils import Configuration
import pprint


class Crawler:
    STATUS_HTTP_DOWN = 500
    MS_LATENCY = 300

    def __init__(self, token: str):
        """ defines crawler properties"""
        self._path = Configuration.findenv('PATH_STORAGE', 'data')
        self._token = token
        self._msg_list = []
        self._channel_list = []
        self._channel_id = ""
        self._guild_id = ""
        self._end_point = ""

    def set_end_point(self, end_point: str):
        """
        set new root end point address
        :param end_point: new end_point
        :return: None
        """
        self._end_point = end_point

    def _special_get(self, url: str, payload: str, headers: dict, tries: int = 3):
        """
        special_get fetch with special strategy
        to handle http responses & possible errors
        recursive function.
        url : url to request
        payload : json params
        tries : nb to try
        """
        do_retry = False
        response = None

        if tries > 0:
            try:
                response = requests.get(url, params=payload, headers=headers)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                do_retry = True
            except Exception:
                raise

            if do_retry or response.status_code >= Crawler.STATUS_HTTP_DOWN:
                sleep(Crawler.MS_LATENCY)
                return self._special_get(url, payload, headers, tries - 1)

        return response

    def fetch_messages(self, channel_id: str, nb_messages: int = 0):
        """
        get specific nb msg from channel
        :param channel_id: id channel
        :param nb_messages: limit of nb msg
        :return: nothing (set list property)
        """
        msg_counter = 0
        payload = {}
        headers = {'Authorization': self._token}
        self._channel_id = channel_id
        self._msg_list = []

        while True:
            try:
                url_end_point = self._end_point.format(channel_id)
                response = self._special_get(url_end_point, str(payload), headers)
                data = response.json()
                nb_read = len(data)

                # if empty or if we get an error
                if nb_read == 0 or type(data) is not list:
                    break

                data.reverse()
                self._msg_list = Scrapper.message_filter(data) + self._msg_list
                payload['before'] = data[0]['id']
                msg_counter = msg_counter + nb_read

                if nb_messages < msg_counter:
                    self._msg_list = self._msg_list[:nb_messages]
                    break
                elif 0 < nb_messages <= msg_counter:
                    break

            except AttributeError as err:
                print("Error: {0}".format(err))
                break

            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                break

    def persist_messages(self):
        """
        Write crawled content on local file
        name is suffixed by the channed id
        :return: nothing
        """
        local_name = "fetch_{}.json".format(self._channel_id)
        full_path = os.path.join(self._path, local_name)
        with open(full_path, 'w') as myfile:
            myfile.write(json.dumps(self._msg_list, ensure_ascii=False).encode('utf8').decode())

    def get_server(self, guild_id):
        """
        get guild (server) info by id
        :param guild_id: id server
        :return: nothing (set guild property)
        """
        headers = {'Authorization': self._token}
        payload = {}
        try:
            url_end_point = self._end_point.format(guild_id)
            response = self._special_get(url_end_point, str(payload), headers)
            self._guild = response.json()

        except AttributeError as err:
            print("Error: {0}".format(err))

        except Exception:
            print("Unexpected error:", sys.exc_info()[0])

    def fetch_channels(self, guild_id: str):
        """
        get all channels from specific guild
        :param channel: id guild
        :return: nothing (set channels list property)
        """
        channels_counter = 0
        payload = {}
        headers = {'Authorization': self._token}
        self._guild_id = guild_id
        self._channel_list = []

        try:
            url_end_point = self._end_point.format(guild_id)
            response = self._special_get(url_end_point, str(payload), headers)
            data = response.json()
            channels_counter = len(data)

            # if empty or if we get an error
            if channels_counter == 0 or type(data) is not list:
                raise Exception('No channel found')

        except AttributeError as err:
            print("Error: {0}".format(err))

        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
