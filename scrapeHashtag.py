from keys import *
from twython import Twython
from twython import TwythonStreamer
import compile
import re

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.CaseyBot.urls


t = Twython(app_key=consumer_key, app_secret=consumer_secret,
            oauth_token=access_token, oauth_token_secret=access_token_secret)


class HashStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            text = data["text"]
            url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
            print url
	    try:
            	compiled_url = compile.doIt(url)
	    	t.update_status(status='@%s : %s'%(data['user']['screen_name'], compiled_url))
	    except:
		print "error in processing"
    def on_error(self, status_code, data):
        print status_code



def activate_stream():
    stream = HashStreamer(consumer_key, consumer_secret,
                          access_token, access_token_secret)
    stream.statuses.filter(track='#CaseyBot')

if __name__ == '__main__':
    activate_stream()
