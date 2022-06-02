class Song:

    def __init__(self, title: str, information: str, verses: dict, source: str):
        self.title = title
        self.information = information
        self.verses = verses
        self.source = source

    def to_dict(self):
        song_dict = {"title": self.title,
                     "information": self.information,
                     "verses": self.verses,
                     "source": self.source
                     }
        return song_dict

    def verses_text(self):
        text = ' '.join(self.verses.values())
        return text


