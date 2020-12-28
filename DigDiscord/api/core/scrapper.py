"""
le scrapper extrait les données du crawler
"""
import hashlib


class Scrapper:
    """
    filtres redefinissant les clés en entrée
    """

    @classmethod
    def message_filter(cls, data):
        """
        filtre pour l'abjet Message
        """
        return [
            {
                "identifier": msg["id"],
                "date": msg["timestamp"][0:10],
                "author": msg["author"]["username"],
                "author_id": msg["author"]["id"],
                "content": msg["content"],
                "references_id": [msg["message_reference"]["message_id"]]
                if "message_reference" in msg
                else [],
                "url": msg["embeds"][0]["url"][0:400]
                if len(msg["embeds"]) > 0
                else None,
                "url_md5": hashlib.md5(
                    (msg["embeds"][0]["url"][0:400]).encode("utf-8")
                ).hexdigest()
                if len(msg["embeds"]) > 0
                else None,
            }
            for msg in data
        ]

    @classmethod
    def link_filter(cls, data):
        """
        filtre pour l'objet Link
        """
        return [
            {"content": msg["embeds"][0]["url"], "message_id": msg["id"]}
            for msg in data
            if len(msg["embeds"]) > 0 and "id" in msg
        ]
