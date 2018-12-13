'''
   Creates plots for tweets and replies from trusted accounts. Only tweets
   with more than 20 replies are included.

   1st plot: Number of tweets (with more than 20 replies) of each account
   2nd plot: Number of replies of each account
'''

from pymongo import MongoClient
import matplotlib.pyplot as plt


connection = MongoClient("mongodb://localhost:27017/")
db = connection.real_news

collections = db.collection_names()


real_tweets_dict = dict()           # dictionary with format key: account name,  value: number of tweets
real_replies_dict = dict()        # dictionary with format key: account name,  value: number of replies



# Create 1st plot
for collection in collections:
    counter = 0
    tweets = db[collection].find().sort("replies_count", -1)

    for tweet in tweets:
        if tweet["replies_count"] > 0:                                      # count tweets with more than 20 replies
            counter += 1
            account_name = tweet["replies"][0]["in_reply_to_screen_name"]    # get account name
    real_tweets_dict[account_name] = counter                                   # set account name as key and number of tweets as value
    print(real_tweets_dict)


plt.bar(range(len(real_tweets_dict)), list(real_tweets_dict.values()), align='center', color=(0.2, 0.6, 0.6, 0.8))
plt.xticks(range(len(real_tweets_dict)), list(real_tweets_dict.keys()))
plt.xticks(rotation=45, ha="right")

#plt.title('Αριθμός των tweets που συλλέχθηκαν από έμπιστους λογαριασμούς')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Tweets')
plt.grid(linestyle=':')
plt.tight_layout()
plt.rc('axes', axisbelow=True)

plt.savefig("../plots/real_tweets_graph.eps")
plt.show()



# Create 2nd plot
for collection in collections:
    replies_count = 0
    tweets = db[collection].find().sort("replies_count", -1)                     # this is optional

    for tweet in tweets:
        if tweet["replies_count"] > 0:                                          # inlude only tweets with more than 20 replies
            account_name = tweet["replies"][0]["in_reply_to_screen_name"]        # get account name
            replies_count = replies_count + tweet["replies_count"]               # add replies count of tweet

    real_replies_dict[account_name] = replies_count                              # set account name as key and number of tweets as value
    print(real_replies_dict)


plt.bar(range(len(real_replies_dict)), list(real_replies_dict.values()), align='center', color=(0.2, 0.6, 0.6, 0.8))
plt.xticks(range(len(real_replies_dict)), list(real_replies_dict.keys()))
plt.xticks(rotation=45, ha="right")

#plt.title('Αριθμός των replies που συλλέχθηκαν από έμπιστους λογαριασμούς')
plt.xlabel('Όνομα λογαριασμού')
plt.ylabel('Replies')
plt.grid(linestyle=':')
plt.tight_layout()
plt.rc('axes', axisbelow=True)

plt.savefig("../plots/real_replies_graph.eps")
plt.show()
