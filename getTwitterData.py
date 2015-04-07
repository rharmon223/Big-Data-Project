# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 09:49:37 2015

@author: zhanx15
"""
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "1954181456-ASXg2Uuze8jKvb58aprggB0qU6Fudeu2uorwZ0o"
access_token_secret = "nfFSNXuMcZQtCiNv3hNwFSjs9Ug0yYSRS3oDRjQgTXdkL"
consumer_key = "aQUsmaLN73IxDIcN6dmJlMQbe"
consumer_secret = "MSJsiwVJg8JFPALy9CC87WhhknaCbwZACK1dJuN1REkguMH0vo"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        with open('twitter.json','a') as tf:
            data = {}
            data['text'] = str(status.text.encode('utf-8').strip())
            data['time'] = str(status.created_at)
            json_data = json.dumps(data)
            tf.write(str(json_data)+'\n')
        print status.author.screen_name, status.created_at, status.text
        
    def on_error(self, status_code):
        print 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print 'Timeout...'
        return True # Don't kill the stream


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = CustomStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['microsoft'])