import requests
import random

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
response.raise_for_status()
WORDS = response.text.splitlines()
longer_random_words = [word for _ in range(250) if (word := random.choice(WORDS)) and len(word) > 3]


class WordList:
    def __init__(self):
        self.words_site = word_site
        self.WORDS = WORDS

    def generate(self, count=250, min_length=3):
        random_words = [word for _ in range(count) if (word := random.choice(self.WORDS)) and len(word) >= min_length]
        return random_words
