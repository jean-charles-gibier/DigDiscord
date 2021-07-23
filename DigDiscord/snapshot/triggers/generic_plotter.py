import re
import json
import random
import requests
import argparse
import tempfile
import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, parameters) -> None:
        if 'filename' not in parameters or parameters['filename'] is None:
            parameters['filename'] = tempfile.NamedTemporaryFile().name
        if 'filetype' not in parameters or parameters['filetype'] is None:
            parameters['filetype'] = 'png'
        self.filename = parameters['filename'] + '.' + parameters['filetype']
        self.headers = {"Authorization": 'Token ' + parameters['token'],
                        "content-type": 'application/json'}
        self.parameters = parameters

    @classmethod
    def get_color(cls):
        """
        pick random (but visible) color
        :param none:
        :return:
        """

        vblue = random.randrange(210)
        vred = random.randrange(210)
        vgreen = random.randrange(210)

        return '#%02x%02x%02x' % (vred, vgreen, vblue)

    @classmethod
    def cm_to_inch(cls, value):
        return value / 2.54

    @property
    def get_filename(self):
        return self.filename

    def set_boundarydates(self):
        """
        set ending and starting dates for following queries to frames a period
        """
        parameters = self.parameters
        startdate = enddate = None
        if 'startdate' in parameters:
            startdate = parameters['startdate']
        if 'enddate' in parameters:
            enddate = parameters['enddate']

        if startdate is None or enddate is None:
            return

        try:
            put_url = self.parameters['url']
            m = re.search(r'([^/]+)/$', put_url)
            g = m.group()
            if g is not None:
                new_url = put_url.replace(g, 'profile/')
            response = requests.put(new_url, headers=self.headers, data='{"date_debut": "' + parameters['startdate']
                                                                        + '", "date_fin": "' + parameters['enddate']
                                                                        + '"}')
        except Exception:
            raise

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error - {response.status_code}")

    def load_data(self):
        """
        load_data get infos from local API
         parameters :
            url : url where to get stats
            payload : add optional infos
            headers : request header mainly set with token info
        """
        try:
            response = requests.get(self.parameters['url'], headers=self.headers)
        except Exception:
            raise

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error - {response.status_code}")

    def draw(self):

        _keys = []
        _values = []
        parameters = self.parameters
        data = json.loads(self.load_data())
        # frame a periode
        self.set_boundarydates()

        if 'results' in data:
            _keys = [i[parameters['name']] for i in data['results']]
            _values = [i[parameters['value']] for i in data['results']]
        else:
            _keys = [i[parameters['name']] for i in data]
            _values = [i[parameters['value']] for i in data]

        plt.figure(figsize=(Plotter.cm_to_inch(35), Plotter.cm_to_inch(15)))
        plt.title(parameters['title'])
        plt.bar(_keys, _values, color=Plotter.get_color())
        plt.xticks(rotation=270)
        plt.tight_layout()
        print(f"save file : {self.filename}")
        plt.savefig(self.filename)


if __name__ == '__main__':
    def parse_arguments():
        """Parse_arguments parsing args
         parameters :
            --url : url where to get stats """
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="""Url where to get stats""", default="")
        parser.add_argument("-v", "--value", help="""Value to aggregate""", default="count")
        parser.add_argument("-n", "--name", help="""Name of aggregation""", default="aggregate_name")
        parser.add_argument("-t", "--title", help="""Title of document""", default="Title")
        parser.add_argument("-fi", "--filename", help="""Name of file""", default=tempfile.TemporaryFile().name)
        parser.add_argument("-y", "--filetype", help="""Type of file""", default="svg")
        parser.add_argument("-k", "--token", help="""Token user""", default="")
        parser.add_argument("-sd", "--startdate", help="""Change starting date""", default="")
        parser.add_argument("-ed", "--enddate", help="""Change ending date""", default="")
        return parser.parse_args()


    args = parse_arguments()
    plotter = Plotter(vars(args))
    plotter.draw()
