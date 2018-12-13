import tweepy
import sys


ACCESS_TOKEN = '927228692140580864-GLpraR3QVnFk1gFkwSjvstmnInETLAj'
ACCESS_SECRET = 'DINNE55cYK8dJB9fGGPXKOGkzswVk6ELExIFp7NoKgxkF'
CONSUMER_KEY = 'UZXHMcTCqtCUrLzS1gZXBT0d8'
CONSUMER_SECRET = 'V6zDhxceIXVOvAkoW9hpGe2jhaMOUFrrfY7R1HphgpyadZEbQF'


auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

if not api:
    print("Can't Authenticate")
    sys.exit(-1)
