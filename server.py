from config import oauth_params
from config import twitter_api_params
import json
import requests
from requests_oauthlib import OAuth1

class PrintServer():
    def __init__(self, consumer_key=oauth_params['consumer_key'], consumer_secret=oauth_params['consumer_secret'], access_token=oauth_params['access_token'], access_token_secret=oauth_params['access_token_secret']):
        print 'initializing printer server'
        self.auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        self.session = requests.Session()

    def _get_user(self, handle):
        handle = json.loads(self.session.get('https://api.twitter.com/1.1/users/lookup.json', auth=self.auth, params={'screen_name':handle}).text)
        found = None
        for entry in handle:
            if 'id' in entry:
                found = entry
        if not found is None:
            return found
        return None

    def run(self):
        print 'establishing connection to Twitter API'
        
        printer = self._get_user(twitter_api_params['printer_handle'])
        if printer is None:
            print 'Error: could not find username "{0}"'.format(twitter_api_params['printer_handle'])
            return
        
        params = {'follow':printer['id']}
        response = self.session.get(url=twitter_api_params['url'], auth=self.auth, params=params, stream=True)
        for line in response.iter_lines():
            print line
            # with open('posts.json', 'wb+') as fw:
                # fw.write(line)
