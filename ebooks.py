import random
import re
import sys
import twitter
import markov
import json
from bs4 import BeautifulSoup
try:
    # Python 3
    from html.entities import name2codepoint as n2c
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from htmlentitydefs import name2codepoint as n2c
    from urllib2 import urlopen
    chr = unichr
from local_settings import *


def connect(type='twitter'):
    if type == 'twitter':
        return twitter.Api(consumer_key=MY_CONSUMER_KEY,
                       consumer_secret=MY_CONSUMER_SECRET,
                       access_token_key=MY_ACCESS_TOKEN_KEY,
                       access_token_secret=MY_ACCESS_TOKEN_SECRET,
                       tweet_mode='extended')
    return None

if __name__ == "__main__":
    guess = 0
    if ODDS and not DEBUG:
        guess = random.randint(0, ODDS - 1)

    if guess:
        print(str(guess) + " No, sorry, not this time.")  # message if the random number fails.
        sys.exit()
    else:
        api = connect()
        source_statuses = []

        if STATIC_TEST:
            file = TEST_SOURCE
            print(">>> Generating from {0}".format(file))
            with open(file, 'r') as f:
                source_statuses = json.load(f)

        if len(source_statuses) == 0:
            print("No statuses found!")
            sys.exit()

        mine = markov.MarkovChainer(ORDER)
        for status in source_statuses:
            mine.add_sentence(status)

        generated_sentence = mine.generate_sentence()

        # if a tweet is very short, this will randomly add a second sentence to it.
        if generated_sentence is not None and len(generated_sentence) < 40:
            rando = random.randint(0, 10)
            if rando >= 7:
                print("Short tweet. Adding another sentence randomly")
                newer_status = mine.generate_sentence()
                if newer_status is not None:
                    generated_sentence += " " + mine.generate_sentence()
                else:
                    generated_sentence = generated_sentence

        # throw out tweets that match anything from the source account.
        if generated_sentence is not None and len(generated_sentence) < 210:
            for status in source_statuses:
                if generated_sentence[:-1] not in status:
                    continue
                else:
                    print("TOO SIMILAR: " + generated_sentence)
                    sys.exit()

            if not DEBUG:
                if ENABLE_TWITTER_POSTING:
                    status = api.PostUpdate(generated_sentence)
            print(generated_sentence)

        elif not generated_sentence:
            print("Status is empty, sorry.")
        else:
            print("TOO LONG: " + generated_sentence)
