"""
Le crawler récupere l'info brute
(tandis que le scrapper lui donne une
consistance en parsant le resulat du crawler)
"""

import json
import os.path
import sys
from time import sleep

import requests
from api.core.content_accessor import ContentAcessor

from .base_utils import Configuration
from .scrapper import Scrapper

import pprint


class Crawler:
    STATUS_HTTP_DOWN = 500
    MS_LATENCY = 300

    def __init__(self, guild_id: str = None, token: str = None, end_point: str = None):
        """ defines crawler properties"""
        self._guild_id = Configuration.findenv("GUILD_ID", guild_id)
        self.server_end_point = Configuration.findenv("GUILD_END_POINT", "NONE")
        self.channel_end_point = Configuration.findenv(
            "CHANNELS_GUILD_END_POINT", "NONE"
        )
        self.message_end_point = Configuration.findenv(
            "MESSAGES_CHANNEL_END_POINT", "NONE"
        )
        self._token = Configuration.findenv("DISCORD_USER_TOKEN", token)
        self._path = Configuration.findenv("PATH_STORAGE", "data")
        self._msg_list = []
        self._link_list = []
        self._channel_list = []
        self._channel_id = ""
        self._guild = ""

    # def set_end_point(self, end_point: str):
    #     """
    #     set new root end point address
    #     :param end_point: new end_point
    #     :return: None
    #     """
    #     self.message_end_point = end_point

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

    def fetch_messages(self, channel_id: str, nb_messages: int = 0, complete_type=None):
        """
        get specific nb msg from channel
        :param channel_id: id channel
        :param nb_messages: limit of nb msg
        :return: nothing (set list property)
        """
        msg_counter = 0
        payload = {}
        headers = {"Authorization": self._token}
        self._channel_id = channel_id
        self._msg_list = []

        if complete_type == "older":
            payload["before"] = ContentAcessor.get_first_message_id(channel_id) or 0
        if complete_type == "newer":
            payload["after"] = ContentAcessor.get_last_message_id(channel_id) or 0

        while True:
            url_end_point = self.message_end_point.format(channel_id)
            print("http req :[end_point='{}' pay_load = '{}' header='{}' ]".format(url_end_point, pprint.pformat(payload ), pprint.pformat(headers)))
            response = self._special_get(url_end_point, payload, headers)
            data = response.json()
            nb_read = len(data)

            print("Recuperation de '{}' messages]".format(nb_read))
            # if empty or if we get an error
            if nb_read == 0 or type(data) is not list:
                break

            data.reverse()

            try:
                self._msg_list = Scrapper.message_filter(data) + self._msg_list
            except KeyError:
                print("Donnee rejetee : [{}]".format(json.dumps(data)))

            if complete_type == "newer":
                payload["after"] = data[-1]["id"]
            else:
                payload["before"] = data[0]["id"]

            msg_counter = msg_counter + nb_read

            if nb_messages < msg_counter:
                self._msg_list = self._msg_list[:nb_messages]
                break
            elif 0 < nb_messages <= msg_counter:
                break

    def get_server(self):
        """
        (public version)
        get server/guild infos
        :return: nothing
        """
        self._get_server()

    def _get_server(self):
        """
        get guild (server) info by id
        :param guild_id: id server
        :return: guild json properties
        """
        headers = {"Authorization": self._token}
        payload = {}
        try:
            url_end_point = self.server_end_point.format(self._guild_id)
            response = self._special_get(url_end_point, str(payload), headers)
            self._guild = response.json()

        except AttributeError as err:
            print("Error: {0}".format(err))

        except Exception:
            print("Unexpected error:", sys.exc_info()[0])

        return self._guild

    def get_channels(self, guild_id: str, store_it: bool = False):
        """
        get all channels from specific guild
        :param guild_id:
        :param channel: id guild
        :param store_it: persist list property
        :return: nothing (set channels list property)
        """
        self._guild_id = guild_id
        self._channel_list = []

        try:

            payload = {}
            headers = {"Authorization": self._token}
            url_end_point = self.channel_end_point.format(guild_id)
            print("http req :[end_point='{}' pay_load = '{}' header='{}']".format(url_end_point, pprint.pformat(payload ), pprint.pformat(headers)))
            response = self._special_get(url_end_point, str(payload), headers)
            self._channel_list = response.json()

            # if cnx err return error
            if type(self._channel_list) is not list:
                raise Exception(
                    'Erreur sur le "end point" {} : {}'.format(
                        url_end_point, str(self._channel_list)
                    )
                )

            # count channels
            channels_counter = len(self._channel_list)
            print("Nombre de channels :{}]".format(channels_counter))

            # if empty or if we get an error
            if channels_counter == 0:
                raise Exception("No channel found")

            if store_it is True:
                self._store_channels()

        except AttributeError as err:
            print("Error channel attribute : {0}".format(err))

        except Exception:
            print(
                "Unexpected error channel :", sys.exc_info()[0], " ", sys.exc_info()[1]
            )

        return self._channel_list

    def store_messages(self):
        """
        Write crawled content on local file
        name is suffixed by the channed id
        :return: nothing
        """
        local_name = "fetch_{}.json".format(self._channel_id)
        full_path = os.path.join(self._path, local_name)
        with open(full_path, "w",  encoding='utf-8') as myfile:
            myfile.write(
                json.dumps(self._msg_list, ensure_ascii=False).encode("utf8").decode()
            )

    def store_server(self):
        """
        (public version)
        Write server content on local file
        :return: nothing
        """
        self._store_server()

    def _store_channels(self):
        """
        Write crawled content on local file
        name is suffixed by the channel id
        :return: nothing
        """
        local_name = "fetch_{}.json".format(self._guild_id)
        full_path = os.path.join(self._path, local_name)
        print("full path store_channels : {}]".format(full_path))
        with open(full_path, "w", encoding='utf-8') as myfile:
            myfile.write(
                json.dumps(self._channel_list, ensure_ascii=False)
                .encode("utf8")
                .decode()
            )

    def _store_server(self):
        """
        Write server infos on local file
        :return: nothing
        """
        local_name = "server_{}.json".format(self._guild_id)
        full_path = os.path.join(self._path, local_name)
        with open(full_path, "w") as myfile:
            myfile.write(
                json.dumps(self._guild, ensure_ascii=False).encode("utf8").decode()
            )
