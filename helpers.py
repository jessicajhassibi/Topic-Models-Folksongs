import jsonlines

from Song import Song


def fill_songbook_from_file(songs_location, songbook):
	with jsonlines.open(songs_location, "r") as json_file:
		for song in json_file:
			song_object = Song(song["title"], song["information"], song["verses"], song["source"])
			if song_object.title in songbook:
				#print("Song:", song_object.title, "already in Songbook.")
				continue
			else:
				songbook[song_object.title] = song_object.to_dict()
	return songbook