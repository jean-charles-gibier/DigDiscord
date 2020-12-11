"""
le scrapper extrait les données du crawler
"""

class Scrapper :
    @classmethod
    def message_filter(cls, data) :
        return [{
        'date': msg['timestamp'],
        'author': msg['author']['username'],
        'content': msg['content'],
        'mentions': msg['mentions']
        } for msg in data]
