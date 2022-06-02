import os
from io import TextIOWrapper
from bs4 import BeautifulSoup
import requests
from Song import Song
import jsonlines


class GutenbergSongsScraper:
    songs = []

    def __init__(self, file, url: str):
        self.file = file
        self.url = url

        # check if songs have been scraped already
        if os.path.isfile(file):
            print("Songs have already been scraped to:", file)
        else:
            with jsonlines.open(file, "w") as jsonl_file:
                print("Scraping from: ", url, "\n")
                self.scrape_book(url, jsonl_file)

    def scrape_song(self, url: str, jsonl_file):
        """
        Scrapes the text content from a chapter of a book of Projekt Gutenberg DE Website (www.projekt-gutenberg.org)
        :param url: The url to the book chapter
        :param txt_file: opened txt file to write chapter to
        :return: txt_file
        """

        html_text = requests.get(url).content
        soup = BeautifulSoup(markup=html_text, features='lxml')

        title = soup.find("h3").text.split("Nr. ")[1].split(" ")[1:]
        song_title = ""
        for word in title:
            if word != " " and word != "" and word != "\n":
                song_title = song_title + word + " "
        song_title = song_title[:-1] # remove last whitespace

        paragraphs = soup.find_all("p") # remove last paragraph, which has just "*" as content
        paragraphs_texts = [p.get_text(strip=True, separator=" ") for p in paragraphs]
        paragraphs_texts = [p for p in paragraphs_texts if p != "" and p != "*"]

        song_information = paragraphs_texts[0]

        song_verses = {}
        verses_list = [p for p in paragraphs_texts[1:] if not p.startswith("[")]
        # TODO: Wiederholte Verse handeln; Handle ";" in Strophen...
        for verse in verses_list:
            # remove repetition signs
            while "|:" in verse:
                verse = verse.replace("|:", "")
            while ":|" in verse:
                verse = verse.replace(":|", "")
            while ":,:" in verse:
                verse = verse.replace(":,:", "")
            # replace common "Dialekt" words TODO: mehr Dialektwörter
            while " i " in verse:
                verse = verse.replace(" i ", " ich ")
            try:
                verse_number = verse.split(". ")[0]
                verse = verse.split(". ")[1]
                # Check sentence ending
                if verse[-1] == "." or verse[-1] == "!" or verse[-1] == "?":
                    verse = verse
                else:
                    if verse[-1] == ";" or verse[-1] == ",":
                        verse = verse[:-1] + "."
                    verse = verse + "."
            except:
                # removing "nonsense" phrases like "Vi-val-le-ra-lal-le-ra-lal-le-ra-la" and additional information
                continue
            song_verses[verse_number] = verse

        new_song = Song(song_title, song_information, song_verses, "Deutschlands Liederschatz")
        song_dict = new_song.to_dict()
        jsonl_file.write(song_dict)
        return jsonl_file

    def scrape_book(self,  url: str, jsonl_file):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        # Find all chapters from the table of contents
        table_of_contents = soup.select("body ul li a")
        # Exclude titlepage
        table_of_contents = table_of_contents[1:]
        for song in table_of_contents:
            song_url = url + song["href"]
            print("Scraping song: ", song_url)
            jsonl_file = self.scrape_song(song_url, jsonl_file)
        print()

    def get_songs(self):
        return self.songs