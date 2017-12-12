import sys
from collections import Counter
import json

from pymongo import MongoClient
from operator import itemgetter
import csv
import os

# from pymongo import MongoClient

# client = MongoClient()
# db = client.test_database  # use a database called "test_database"
# collection = db.files   # and inside that DB, a collection called "files"

# f = open('data.csv')  # open a file
# text = f.read()    # read the entire contents, should be UTF-8 text

# #build a document to be inserted
# text_file_doc = {"file_name": "data.txt", "contents" : text }
# #insert the contents into the "file" collection
# collection.insert(text_file_doc)



def get_mentions(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]

    
#with open('mentions.csv','wb') as file


if __name__ == '__main__':
    i = 0
    fname = sys.argv[1]
    file = open('mentions.csv', 'w')
    with open(fname, 'r') as f:
        users = Counter()
        for line in f:
            tweet = json.loads(line)
            mentions_in_tweet = get_mentions(tweet)
            users.update(mentions_in_tweet)
        for user, count in users.most_common(80):
            i = i+1
            print("{}: {}".format(user, count))
            file.write(user + ',' + str(count) + '\n')
    file.close()
