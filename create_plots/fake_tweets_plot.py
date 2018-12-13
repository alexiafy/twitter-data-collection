'''
   Creates plots for tweets and replies from not trusted accounts. Only tweets
   with more than 20 replies are included.

   1st plot: Number of tweets (with more than 20 replies) of each account
   2nd plot: Number of replies of each account
'''

from pymongo import MongoClient
import matplotlib.pyplot as plt
from api import api
import tweepy

connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news

collections = db.collection_names()


# Exception message
def getExceptionMessage(msg):
    words = msg.split(' ')

    error_msg = ""
    for index, word in enumerate(words):
        if index not in [0,1,2]:
            error_msg = error_msg + ' ' + word
    error_msg = error_msg.rstrip("\'}]")
    error_msg = error_msg.lstrip(" \'")

    return error_msg


fake_tweets_dict = dict()           # dictionary with format key: account name,  value: number of tweets
fake_replies_dict = dict()        # dictionary with format key: account name,  value: number of replies


# Create 1st plot
for collection in collections:
    counter = 0

    tweets = db[collection].find().sort("replies_count", -1)
    number_of_documents = db[collection].count()          # count the number of tweets of the account

    if number_of_documents > 0:                           # if the account has at least one tweet
        for tweet in tweets:
            if tweet["replies_count"] > 0:                                     # count tweets with more than 20 replies
                counter += 1
                account_name = tweet["replies"][0]["in_reply_to_screen_name"]            # get account name
                fake_tweets_dict[account_name] = counter         # set account name as key and number of tweets as value
        print(fake_tweets_dict)
    else:                                                      # if the account does not have any tweets
        try:
            user = api.get_user(collection)
            fake_tweets_dict[user.screen_name] = 0               # set the number of tweets of the account to 0
            print(fake_tweets_dict)
        except tweepy.TweepError as e:
            print(e.api_code)
            print(getExceptionMessage(e.reason))


plt.bar(range(len(fake_tweets_dict)), list(fake_tweets_dict.values()), align='center', color=(0.2, 0.6, 0.6, 0.8))
plt.xticks(range(len(fake_tweets_dict)), list(fake_tweets_dict.keys()))
plt.xticks(rotation=45, ha="right")

#plt.title('Αριθμός των tweets που συλλέχθηκαν από μη έμπιστους λογαριασμούς')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Tweets')
plt.grid(linestyle=':')
plt.tight_layout()
plt.rc('axes', axisbelow=True)

plt.savefig("../plots/fake_tweets_graph.eps")
plt.show()


# Create 2nd plot
for collection in collections:
    replies_count = 0

    tweets = db[collection].find().sort("replies_count", -1)
    number_of_documents = db[collection].count()                         # count the number of tweets of the account

    if number_of_documents > 0:                                          # if the account has at least one tweet
        for tweet in tweets:
            if tweet["replies_count"] > 0:                                 # count tweets with more than 20 replies
                account_name = tweet["replies"][0]["in_reply_to_screen_name"]       # get account name
                replies_count = replies_count + tweet["replies_count"]
                fake_replies_dict[account_name] = replies_count            # set account name as key and number or tweets as value
        print(fake_replies_dict)
    else:                                                          # if the account does not have any tweets and replies
        try:
            user = api.get_user(collection)
            fake_replies_dict[user.screen_name] = 0                     # set the number of replies of the account to 0
            print(fake_replies_dict)
        except tweepy.TweepError as e:
            print(e.api_code)
            print(getExceptionMessage(e.reason))


plt.bar(range(len(fake_replies_dict)), list(fake_replies_dict.values()), align='center', color=(0.2, 0.6, 0.6, 0.8))
plt.xticks(range(len(fake_replies_dict)), list(fake_replies_dict.keys()))
plt.xticks(rotation=45, ha="right")

#plt.title('Αριθμός των replies που συλλέχθηκαν από μη έμπιστους λογαριασμούς')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Replies')
plt.grid(linestyle=':')
plt.tight_layout()
plt.rc('axes', axisbelow=True)

plt.savefig("../plots/fake_replies_graph.eps")
plt.show()
