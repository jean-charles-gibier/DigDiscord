"""
le scrapper extrait les données du crawler
"""

class Scrapper :
    @classmethod
    def message_filter(cls, data):
        return [{
        'date':  msg['timestamp'][0:10],
        'author': msg['author']['username'],
        'author_id': msg['author']['id'],
        'content': msg['content'],
        'mentions': msg['mentions']
        } for msg in data]
