import os

import jsonlines
import requests
import wikipediaapi
from bs4 import BeautifulSoup, element

from Song import Song


class WikipediaSongsScraper:
	wiki_wiki = wikipediaapi.Wikipedia(
		language="de",
		extract_format=wikipediaapi.ExtractFormat.WIKI
	)
	songs = []

	def __init__(self, page: str, location: str):
		self.wiki_page = self.wiki_wiki.page(page)
		self.location = location
		self.titles = self.wiki_page.links

		# check if songs have been scraped already
		if os.path.isfile(location):
			print("Songs has already been scraped to:", location)
		else:
			with jsonlines.open(location, "w") as jsonl_file:

				for title in self.titles:
					if " (Lied)" in title:
						title = title.replace(" (Lied)", "")
					elif " (Volkslied)" in title:
						title = title.replace(" (Volkslied)", "")

					# Uses requests library for extracting HTML
					# Not used Wikipedia API for extracting HTML (song_page = html_wiki.page(title)) because doesn't show songtext
					url = "https://de.wikipedia.org/wiki/" + title.replace(" ", "_")
					print("Scraping song from Wikipedia:", url)
					html_text = requests.get(url).content
					soup = BeautifulSoup(markup=html_text, features='lxml')

					# Scraping verses
					verses = []

					try:
						songtext = soup.find("div", {"class": "poem"}).find("p").contents
						verse = ""
						for line in songtext:
							if isinstance(line, element.NavigableString):
								verse = verse + line
								if line == "\n":
									verse = verse.replace("\n", " ")[:-1]
									if verse != "":
										verses.append(verse)
										verse = ""
					except:
						# if no text exists, take title as verse, so at least some topic information can be taken from title
						verses = [title + "."]

					verses_dict = dict()
					for i in range(len(verses)):
						verses_dict[str(i + 1)] = verses[i]
					print()

					new_song = Song(title, "info", verses_dict, "Wikipedia Volkslieder-Liste")
					self.songs.append(new_song)
					song_dict = new_song.to_dict()
					jsonl_file.write(song_dict)

	def get_songs(self):
		return self.songs