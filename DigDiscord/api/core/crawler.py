"""
Le crawler récupere l'info brute
(tandis que le scrapper lui donne une
consistance en parsant le resulat du crawler)
"""

from time import sleep
import requests
import codecs
import sys
import json


class Crawler:

    def __init__(self, d_token: str, d_end_point: str):
        """ defines config properties"""
        self.d_token = d_token
        self.d_end_point = d_end_point
        self.msg_list = []
        self.channel = ""


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

            if do_retry or response.status_code >= 500:
                sleep(300)
                return self._special_get(url, payload, headers, tries - 1)

        return response

    def fetch(self, channel: str, nb_messages: int = 0):
        """
        get specific nb msg from channel
        :param channel: id channel
        :param nb_messages: limit of nb msg
        :return:
        """
        msg_counter = 0
        payload = {}
        headers = {'Authorization': self.d_token}
        self.channel = channel
        self.msg_list = []

        while True:
            try:
                url_end_point = self.d_end_point.format(channel)
                response = self._special_get(url_end_point, payload, headers)
                data = response.json()
                nb_read = len(data)

                if nb_read == 0:
                    break

                data.reverse()
                self.msg_list = [{
                    'date': msg['timestamp'],
                    'author': msg['author']['username'],
                    'content': msg['content'],
                    'mentions': msg['mentions']
                } for msg in data] + self.msg_list

                payload['before'] = data[0]['id']
                msg_counter = msg_counter + nb_read

                if nb_messages < msg_counter:
                    self.msg_list = self.msg_list[:nb_messages]
                    break
                elif 0 < nb_messages <= msg_counter:
                    break

            except AttributeError as err:
                print("Unexpected error: {0}".format(err))
                break

            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                break


    def persist(self):
        """
        write crawled content
        :return:
        """
        w = codecs.getwriter("utf-8")(sys.stdout.buffer)
        with open("fetch_{}.json".format(self.channel), 'w') as myfile:
            myfile.write(json.dumps(self.msg_list))
