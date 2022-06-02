import json
from Song import Song
import nltk

class Songbook:
	songtexts = []
	sentences = []
	songs = []
	verses = []

	def __init__(self, songs_dict):
		self.songs_dict = songs_dict

		for key in songs_dict.keys():
			song = self.songs_dict[key]
			song_object = Song(song["title"], song["information"], song["verses"], song["source"])
			self.songs.append(song_object)

		for song in self.songs:
			self.songtexts.append(song.verses_text())

		for songtext in self.songtexts:
			sentences = nltk.sent_tokenize(songtext)
			for sentence in sentences:
				self.sentences.append(sentence)

	def get_songtexts(self):
		return self.songtexts

	def get_sentences(self):
		return self.sentences

	def get_size(self):
		return len(self.songs)