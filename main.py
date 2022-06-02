# Topic Modeling on Folk Songs

import gutenberg_scraper
from Songbook import Songbook
from bertopic import BERTopic
from top2vec import Top2Vec
import wikipedia_scraper
import jsonlines
import helpers
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
# Download nltk "stopwords" corpus if not done before
#nltk.download()


if __name__ == '__main__':
    # Initialize songbook
    songbook = {}

    # Scrape Songbook from Project Gutenberg
    # define books as tuples of url and path with filename
    songbook_url = "https://www.projekt-gutenberg.org/antholog/dtlieder/"
    gutenberg_songs_location = "data/scraped_songs/Gutenberg_Songs.json"

    # Instantiate Scraper
    gutenberg_song_scraper = gutenberg_scraper.GutenbergSongsScraper(gutenberg_songs_location, songbook_url)

    songbook = helpers.fill_songbook_from_file(gutenberg_songs_location, songbook)

    print("##################################################################################\n")


    # Scrape Songs from Wikipedia "Volkslieder"-Liste
    page = "Liste von Volksliedern"
    wikipedia_songs_location = "data/scraped_songs/Wikipedia_Songs.json"
    wikipedia_song_scraper = wikipedia_scraper.WikipediaSongsScraper(page, wikipedia_songs_location)

    songbook_dict = helpers.fill_songbook_from_file(wikipedia_songs_location, songbook)

    print("##################################################################################\n")

    # Save Songbook
    #with jsonlines.open("data/Songbook.json", "w") as songbook_file:
    #    songbook_dict = dict(songbook)
    #    songbook_file.write(songbook_dict)

    # Load Songbook
    #with jsonlines.open("data/Songbook.json", "r") as songbook_file:
    #    songbook_dict = songbook_file.read()

    #songbook = Songbook(songbook_dict)
    #print("Created songbook with", songbook.get_size(), "songs with", str(len(songbook.get_sentences())), "sentences.")

    # Topic modeling with BERTopic
    # Best model:
    #topic_model = BERTopic(verbose=True, language="german")
    #topics, probs = topic_model.fit_transform(all_sentences)
    #topic_model = BERTopic.load("BERTopic_models/german")
    #topic_model.save("BERTopic_models/german")

    #german_stop_words = stopwords.words('german')
    #vectorizer_model = CountVectorizer(stop_words=german_stop_words)
    #topic_model = BERTopic(verbose=True, language="multilingual", vectorizer_model=vectorizer_model)
    #topics, probs = topic_model.fit_transform(songbook.get_sentences())
    #topic_model = BERTopic.load("BERTopic_models/german")
    #topic_model.save("BERTopic_models/multilingual")

    # Top2Vec approach
    #top2vec_model = Top2Vec(songbook.get_sentences())
    #top2vec_model.save("Top2Vec_models/model")

    # TODO: Verbessere Top2Vec ergebnis
    # TODO Zahlen entfernen aus Versen
    # TODO fremde Sprachen entfernen
    # TODO ganze Verse als Input