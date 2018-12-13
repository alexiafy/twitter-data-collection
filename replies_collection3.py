'''
    Collect fake tweets -  third attempt with the same accounts.
    We don't create the collections.
'''

from api import api
import pymongo
import csv
import tweepy
import datetime

uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(uri)
db = client.trial_news                     #TODO Change the database
collections = db.collection_names()

def take_user_tweets():
    pages = 100   #TODO change to 100
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    for user in all_users:
        print(user[0])
        for page in range(1, pages):
            print(page)
            try:
                new_tweets = api.user_timeline(id=user[0], page=page, count=200)     # get the tweets
            except Exception as e:
                print("Something went wrong...")
                print(e)

            if not new_tweets:
                print("No more tweets found")
                break

            # If tweet's datetime is within the last 7 days, insert it to the database, else break
            for tweet in new_tweets:
                if not tweet.retweeted:                                     # check if the tweet is retweet
                    if tweet.created_at > seven_days_ago:
                        db[user[0]].insert_one(tweet._json)                 # insert tweet into database
                        db[user[0]].update({"id": tweet.id}, {"$set": {"replies_count": 0}})    # set replies_count field
                    else:
                        break

            # If the last tweet is older than 7 days, break the loop and continue with the next account
            if new_tweets[len(new_tweets)-1].created_at < seven_days_ago:
                break


def take_user_replies():
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    all_replies_sum = 0      # sum of all the replies collected
    for user in all_users:
        if user[0] in collections:
            continue
        user_replies_count = 0  # counts the replies of each user account

        max_tweets = 5000     # TODO change to 5000
        tweets_per_qry = 100  # this is the max the API permits

        # If results from a specific ID onwards are reqd, set since_id to that ID.
        # else default to no lower limit, go as far back as API allows
        since_id = None

        # If results only below a specific ID are, set max_id to that ID.
        # else default to no upper limit, start from the most recent tweet matching the search query.
        max_id = -1000000
        str1 = "to:"                 # or "@"
        str2 = user[2]               # the 3rd word of csv is the "reply name"
        search_query = str1 + str2

        tweet_count = 0
        print("Downloading max {0} tweets".format(max_tweets))
        while tweet_count < max_tweets:
            try:
                if max_id <= 0:
                    if not since_id:
                        new_replies = api.search(q=search_query, count=tweets_per_qry)
                    else:
                        new_replies = api.search(q=search_query, count=tweets_per_qry,
                                                 since_id=since_id)
                else:
                    if not since_id:
                        new_replies = api.search(q=search_query, count=tweets_per_qry,
                                                 max_id=str(max_id - 1))
                    else:
                        new_replies = api.search(q=search_query, count=tweets_per_qry,
                                                 max_id=str(max_id - 1), since_id=since_id)

                if not new_replies:
                    print("No more tweets found")
                    break

                # For each reply, find the tweet that is replied to and insert the reply to the database
                # and add +1 to the reply_count of the tweet
                for reply in new_replies:
                    tweets = db[user[0]].find()
                    for tweet in tweets:
                        if reply.in_reply_to_status_id == tweet["id"]:
                            db[user[0]].update({"id": tweet["id"]}, {"$addToSet": {"replies": reply._json}})           # insert the reply to database
                            replies_count = db[user[0]].find_one({'id': tweet["id"]},                  # read the reply_count of the tweet from the database
                                                                 {"_id": 0, "replies_count": 1})["replies_count"]
                            db[user[0]].update({"id": tweet["id"]}, {'$set': {"replies_count": replies_count + 1}})     # insert the new reply_count to database
                            user_replies_count = user_replies_count + 1

                tweet_count += len(new_replies)
                print("Downloaded {0} tweets".format(tweet_count))

                max_id = new_replies[-1].id

                if new_replies[len(new_replies) - 1].created_at < seven_days_ago:
                    break
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

        all_replies_sum = all_replies_sum + user_replies_count
        # Write results to file
        file = open("results/results_fake_news2.txt", "a")
        file.write(user[0])
        file.write(", ")
        file.write(user[2])
        file.write(", ")
        file.write("replies: ")
        file.write(str(user_replies_count))
        file.write("\n")
        file.close()

    # Write results to file
    file = open("results/results_trials_news2.txt", "a")
    file.write("Sum of all tweets: ")
    file.write(str(all_replies_sum))
    file.close()

# read real news accounts from csv file
with open('input/real news accounts trials.csv', 'r', encoding="utf8") as csvFile:  #TODO Change the file name
    reader = csv.reader(csvFile, delimiter=',')
    all_users = list(reader)    # convert csv reader object to list

    #file = open("results/results_fake_news2.txt", "w")
    #file.close()

    take_user_tweets()
    take_user_replies()







