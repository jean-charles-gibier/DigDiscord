"""
le scrapper extrait les données du crawler
"""


class Scrapper:
    """
    filtres redefinissant les clés en entrée
    """

    @classmethod
    def message_filter(cls, data):
        """
        filtre pour l'aobjet Message
        """
        return [
            {
                "identifiant": msg["id"],
                "date": msg["timestamp"][0:10],
                "author": msg["author"]["username"],
                "author_id": msg["author"]["id"],
                "content": msg["content"],
                "mentions": msg["mentions"],
                "url": msg["embeds"][0]["url"][0:300]
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
            {"content": msg["embeds"][0]["url"], "id": msg["id"]}
            for msg in data
            if len(msg["embeds"]) > 0
        ]
