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

    def _special_get(self, url: str, payload: str, headers: dict, tries: int = 3):
        """
        special_get fetch with special strategy
        to handle http responses & possible errors
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
                return self.special_get(url, payload, tries - 1)

        return response

    def fetch(self, channel: str, nb_messags: int = 0, chunk_size: int = 50) -> str:
        w = codecs.getwriter("utf-8")(sys.stdout.buffer)

        _last_msg_number = 0
        _msg_counter = 0
        payload = {}
        headers = {'Authorization': self.d_token}
        print('CHECK : {} TOKEN : {} ... '.format(channel, self.d_token))

        big_bag_msg = []

        while True:
            try:
                response = self._special_get(
                    self.d_end_point.format(channel),
                    payload,
                    headers)
                data = response.json()
                _last_msg_number = _last_msg_number + 1
                data.reverse()

                big_bag_msg = [{
                    'date': msg['timestamp'],
                    'author': msg['author']['username'],
                    'content': msg['content'],
                    'mentions': msg['mentions']
                } for msg in data] + big_bag_msg

                payload['before'] = data[0]['id']
                _msg_counter = _msg_counter + len(data)

                if nb_messags < _msg_counter:
                    big_bag_msg = big_bag_msg[:_msg_counter]
                    break
                if len(data) < chunk_size:
                    break
                else:
                    print('Getting {} msg before {} ... '.format(chunk_size, payload['before']))

            except AttributeError as err:
                print("Unexpected error: {0}".format(err))
                break
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
# write a part
        with open("fetch_{}.json".format(channel), 'w') as myfile:
            myfile.write(json.dumps(big_bag_msg))
