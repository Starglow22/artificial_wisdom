from os import environ

'''
Local Settings for a twitter account. 
'''

# Configuration for Twitter API
ENABLE_TWITTER_POSTING = True # Tweet resulting status?
MY_CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY')#Your Twitter API Consumer Key set in Heroku config
MY_CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET')#Your Consumer Secret Key set in Heroku config
MY_ACCESS_TOKEN_KEY = environ.get('TWITTER_ACCESS_TOKEN_KEY')#Your Twitter API Access Token Key set in Heroku config
MY_ACCESS_TOKEN_SECRET = environ.get('TWITTER_ACCESS_SECRET')#Your Access Token Secret set in Heroku config

# Sources (Twitter, local text file or a web page)
STATIC_TEST = True  # Set this to True if you want to test Markov generation from a static file instead of the API.
TEST_SOURCE = "alan_watts.json"  # The name of a json file of an array of string data

ODDS = 10  # How often do you want this to run? 1/8 times?
ORDER = 2  # How many words is a state? How closely do you want this to be to sensical? 2 is low and 4 is high.

DEBUG = False  # Set this to False to start Tweeting live
TWEET_ACCOUNT = "artificial_wisdom"  # The name of the account you're tweeting to.
