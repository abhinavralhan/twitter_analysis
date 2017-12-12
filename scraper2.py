# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream

# access_token = "98341825-qv8wF5hwRCGRrTpzxP7fes4nJ1g9rjHFyBuHOzFbu"
# access_token_secret = "WW5SQKeJxuqdNr3vJ8ybNCPAYqOiCHDz2XLhMtnszVzNj"
# consumer_key = "PdAKVXyxZAlzHQkH62RhgkuBY"
# consumer_secret = "P0qJdJmzclI6otwiApVee7UcjWl4GcZa8GkGWHoV4IdOyjsfM1"


# class StdOutListener(StreamListener):

#     def on_data(self, data):
#         print(data)
#         return True

#     def on_error(self, status):
#         print(status)


# if __name__ == '__main__':

#     l = StdOutListener()
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     stream = Stream(auth, l)

#     stream.filter(track=['#DelhiSmog', '#OddEven', '#DelhiPollution', '#Delhipollution', '#MumbaiRains', '#CycloneOckhi', '#CropBurning'])


from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/mumbairain'  # assuming you have mongoDB installed locally

#['#DelhiSmog', '#OddEven', '#DelhiPollution', '#Delhipollution', '#Smog', '#oddeven', '#delhipollution']
WORDS = ['#Mumbai', '#MumbaiRains', '#CycloneOckhi', '#MumbaiRains', '#Bombay', '#mumbairain', 'Cyclone Ockhi', '#BombayRain', 'Mumbai Rains', '#cyclone', '#ockhi', '#Ockhi', 'Mumbai flood', 'Sea link', '#Bandra', '#Worli', '#MumbaiSmog']


keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
#print(consumer_key)
consumer_secret = lines[1].rstrip()
#print(consumer_secret)
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.mumbairain

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
