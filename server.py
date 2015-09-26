from config import oauth_params
from config import twitter_api_params
import requests
from requests_oauthlib import OAuth1

class PrintServer():
    def __init__(self, consumer_key=oauth_params['consumer_key'], consumer_secret=oauth_params['consumer_secret'], access_token=oauth_params['access_token'], access_token_secret=oauth_params['access_token_secret']):
        print 'initializing printer server'
        self.auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        self.session = requests.Session()

    def run(self):
        print 'establishing connection to Twitter API'
        params = {'follow':twitter_api_params['printer_handle'], 'track':'print', 'stringify_friend_ids':'true'}
        response = self.session.get(url=twitter_api_params['url'], auth=self.auth, params=params, stream=True)
        for line in response.iter_lines():
            with open('posts.json', 'wb+') as fw:
                fw.write(line)