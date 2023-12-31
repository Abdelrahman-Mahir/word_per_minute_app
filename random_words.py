import requests
import random

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
response.raise_for_status()
WORDS = response.text.splitlines()
longer_random_words = [word for _ in range(5000) if (word := random.choice(WORDS)) and len(word) > 3]


class WordList:
    def __init__(self):
        self.words_site = word_site
        self.WORDS = WORDS

    def generate(self, count=1000, min_length=3, max_length=6):
        random_words = [word for _ in range(count) if
                        (word := random.choice(self.WORDS)) and min_length < len(word) < max_length]
        return random_words
