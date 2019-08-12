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


def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return chr(int(text[3:-1], 16))
            else:
                return chr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        if guess == "apos":
            guess = "lsquo"
        numero = n2c[guess]
        try:
            text = chr(numero)
        except KeyError:
            pass
    return text


def filter_status(text):
    text = re.sub(r'\b(RT|MT) .+', '', text)  # take out anything after RT or MT
    text = re.sub(r'(\#|@|(h\/t)|(http))\S+', '', text)  # Take out URLs, hashtags, hts, etc.
    text = re.sub('\s+', ' ', text)  # collaspse consecutive whitespace to single spaces.
    text = re.sub(r'\"|\(|\)', '', text)  # take out quotes.
    text = re.sub(r'\s+\(?(via|says)\s@\w+\)?', '', text)  # remove attribution
    text = re.sub(r'<[^>]*>','', text) #strip out html tags from mastodon posts
    htmlsents = re.findall(r'&\w+;', text)
    for item in htmlsents:
        text = text.replace(item, entity(item))
    text = re.sub(r'\xe9', 'e', text)  # take out accented e
    return text




def grab_tweets(api, max_id=None):
    source_tweets = []
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    if user_tweets:
        max_id = user_tweets[-1].id - 1
        for tweet in user_tweets:
            if tweet.full_text:
                tweet.text = filter_status(tweet.full_text)
            else:
                tweet.text = filter_status(tweet.full_text)
            if re.search(SOURCE_EXCLUDE, tweet.text):
                continue
            if tweet.text:
                source_tweets.append(tweet.text)
    else:
        pass
    return source_tweets, max_id

def grab_toots(api, account_id=None,max_id=None):
    if account_id:
        source_toots = []
        user_toots = api.account_statuses(account_id)
        max_id = user_toots[len(user_toots)-1]['id']-1
        for toot in user_toots:
            if toot['in_reply_to_id'] or toot['reblog']:
                pass #skip this one
            else:
                toot['content'] = filter_status(toot['content'])
                if len(toot['content']) != 0:
                    source_toots.append(toot['content'])
        return source_toots, max_id

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
