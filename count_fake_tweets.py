'''
   Counts number of tweets and replies from not trusted accounts. Only tweets
   with more than 20 replies are included.
'''

from pymongo import MongoClient


connection = MongoClient("mongodb://localhost:27017/")
db = connection.fake_news


collections = db.collection_names()


# Count the tweets that have more than 20 replies from each account.
file = open("Results/FN - Number of tweets (only tweets with more than 20 replies).txt", "w")
total_count = 0
for collection in collections:
    counter = 0
    file.write("Account id: ")
    file.write(collection)
    tweets = db[collection].find().sort("replies_count", -1)
    for tweet in tweets:
        if tweet["replies_count"] > 20:
            counter += 1
    total_count += counter
    file.write(", Tweets: ")
    file.write(str(counter))
    file.write("\n")

file.write("\nSum of all tweets: ")
file.write(str(total_count))
file.close()


# Count the replies of each tweet of each account. Only the tweets that have more than 20 replies.
file = open("Results/FN - Number of replies of tweets (only tweets with more than 20 replies).txt", "w")
replies_count = 0
for collection in collections:
    file.write("Account id: ")
    file.write(collection)
    file.write("\n")
    tweets = db[collection].find().sort("replies_count", -1)
    for tweet in tweets:
        if tweet["replies_count"] > 20:
            file.write("Tweet id: ")
            file.write(tweet["id_str"])
            file.write(", Replies: ")
            file.write(str(tweet["replies_count"]))
            file.write("\n")
            replies_count = replies_count + tweet["replies_count"]


file.write("Sum of all replies: ")
file.write(str(replies_count))
file.close()



'''file = open("Results/Count tweets of each account.txt", "w")
tweets_count = 0
for collection in collections:
    print("Account: ", collection)
    print("Count of all tweets: ", db[collection].find().count())
    file.write("Account id: ")
    file.write(collection)
    file.write(", Tweets: ")
    file.write(str(db[collection].find().count()))
    file.write("\n")
    tweets_count += db[collection].find().count()

file.write("\nSum of all tweets: ")
file.write(str(tweets_count))
file.close()


file = open("Results/Count replies of each account.txt", "w")
replies_count = 0
for collection in collections:
    file.write("Account id: ")
    file.write(collection)
    file.write("\n")
    tweets = db[collection].find().sort("replies_count", -1)
    for tweet in tweets:
        file.write("Tweet id: ")
        file.write(tweet["id_str"])
        file.write(", Replies: ")
        file.write(str(tweet["replies_count"]))
        file.write("\n")
        replies_count = replies_count + tweet["replies_count"]


file.write("Sum of all replies: ")
file.write(str(replies_count))
file.close()'''
