import config
import json
import ast
import requests
import thread
import random
import string
from requests_oauthlib import OAuth1
import win32print
import tempfile
import win32api

class PrintServer():
    def __init__(self, consumer_key=config.consumer_key, consumer_secret=config.consumer_secret, access_token=config.access_token, access_token_secret=config.access_token_secret):
        print '\n\n___________________# Print___________________\n\n\ninitializing printer server...\n'
        self.auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        self.session = requests.Session()

    def _get_user(self, handle):
        handle = json.loads(self.session.get('https://api.twitter.com/1.1/users/lookup.json', auth=self.auth, params={'screen_name':handle}).text)
        found = None
        for entry in handle:
            if 'id' in entry:
                found = entry
        if found is not None:
            return found
        return None

    def _is_valid_post(self, post):
        entities = 'entities' in post
        mentions = 'user_mentions' in post['entities']
        hasPrinter = self.printer['id'] in [user['id'] for user in post['entities']['user_mentions']]
        fromValid = 'user' in post and 'id' in post['user'] and post['user']['screen_name'].lower() in self.valid_users
        text = 'text' in post
        hashtags = 'hashtags' in post['entities']

        return (entities and mentions and hasPrinter and fromValid and text and hashtags)
    
    def _parse_post(self, post):
        hashtags = post.getHashtags()
        if 'help' in hashtags:
            self._help(post.getSender())
            return
        elif 'grant' in hashtags:
            self._grant_access(post, post.getSender())
            self._update_users(self.users_file)
            return
        elif 'revoke' in hashtags:
            self._revoke_access(post, post.getSender())
            self._update_users(self.users_file)
            return
        elif 'print' in hashtags:
            copies = 1
            if 'copy' in hashtags:
                try:
                    copies = int(post.getAfterTag('copy').strip())
                except:
                    params = {'status':'{1} @{0}, text after #copy must be an integer number'.format(post.getSender(), ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))}
                    requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params)
            if 'raw' in hashtags:
                self._print_raw(post, copies)
            #'pdf' in hashtags and 'img' in hashtag and 'web' in 
        return

    def _help(self, sender):
        if sender.lower() == config.super_sender:
            params1 = {'status':'{1} @{0}, #print creates a new print job; use #raw, #pdf, #img, or #web to specify file type'.format(sender, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))[:140]}
            params2 = {'status':'{1} @{0}, #copy specifies number of copies you would like to print'.format(sender, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))[:140]}
            params3 = {'status':'{1} @{0}, #grant gives print access to anyone mentioned; #revoke revokes access'.format(sender, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))[:140]}
            requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params1)
            requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params2)
            requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params3)
        else:
            params1 = {'status':'{1} @{0}, #print creates a new print job; use #raw, #pdf, #img, or #web to specify file type'.format(sender, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))[:140]}
            params2 = {'status':'{1} @{0}, #copy specifies number of copies you would like to print'.format(sender, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))[:140]}
            requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params1)
            requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params2)
        print 'sent help data to {0}'.format(sender)
        return
        
    def _grant_access(self, post, sender):
        if sender.lower() == config.super_sender:
            mentions = post.getMentions()
            for user in mentions:
                user = user['screen_name'].lower()
                if user not in self.valid_users:
                    self.valid_users.append(user)
                    params = {'status':'{2} @{0}, you have just given @{1} access to use your printer'.format(post.getSender(), user, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))}
                    requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params)
            print 'granted access for the following users: {0}'.format(mentions)
        return
        
    def _revoke_access(self, post, sender):
        if sender.lower() == config.super_sender:
            mentions = post.getMentions()
            for user in mentions:
                user = user['screen_name'].lower()
                if user in self.valid_users:
                    self.valid_users.remove(user)
                    params = {'status':'{2} @{0}, @{1} no longer has access to use your printer'.format(post.getSender(), user, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))}
                    requests.post(url='https://api.twitter.com/1.1/statuses/update.json', auth=self.auth, data=params)
            print 'revoked access for the following users: {0}'.format(mentions)
        return

    def _update_users(self, users_file):
        with open(users_file, 'wb+') as writer:
            for item in self.valid_users:
                writer.write('{0}\n'.format(item))
        return
    
    def _print_raw(self, post, copies):
        print 'printing raw text...'
        for i in range(0,copies):
            filename = tempfile.mktemp ("raw.txt")
            open (filename, "w").write (post.getUntaggedText())
            win32api.ShellExecute (0,"printto",filename,'"{0}"'.format(config.printer_name),".",0)
        return

    def load_users(self, users_file):
        self.users_file = users_file
        print 'loading list of valid users...\n'
        self.valid_users = []
        with open(users_file) as reader:
            for line in reader:
                u = self._get_user(line)
                if u is not None:
                    self.valid_users.append(u['screen_name'].lower())

    def run(self):
        print 'establishing connection to Twitter API...\n'
        
        self.printer = self._get_user(config.printer_handle)
        if self.printer is None:
            print 'Error: could not find username "{0}"'.format(config.printer_handle)
            return
        else:
            print 'printer user "{0}" found'.format(self.printer['screen_name'])

        print 'opening Twitter stream...\n'
        params = {'track':self.printer['screen_name']}
        stream = self.session.post(url=config.url, auth=self.auth, data=params, stream=True)
        for line in stream.iter_lines():
            if line:
                post = json.loads(line)
                if self._is_valid_post(post):
                    print 'post recieved:\n\ttext: {0}\n'.format(post['text'])
                    post = Post(post, self.printer)               
                    self._parse_post(post)


class Post():
    def __init__(self, post, printer):
        self.sender = post['user']['screen_name']
        self.text = post['text']
        self.hashtags = post['entities']['hashtags']
        self.user_mentions = [user for user in post['entities']['user_mentions'] if user['id'] != printer['id']]
        self.urls = post['entities']['urls']
    def getSender(self):
        return self.sender
    def getText(self):
        return self.text
    def getHashtags(self):
        if self.hashtags != []:
            return [tag['text'] for tag in self.hashtags]
        else:
            return []
    def getMentions(self):
        return self.user_mentions
    def getUrls(self):
        return self.urls
    def getUntaggedText(self):
        output = self.text
        for tag in self.hashtags:
            if tag['text'] == 'copy':
                output = output[:tag['indices'][0]]
        for hashtag in self.hashtags:
            output = output[:hashtag['indices'][0]] + output[hashtag['indices'][1]:]
        for mention in self.user_mentions:
            output = output[:mention['indices'][0]] + output[mention['indices'][1]:]
        return output
    def getAfterTag(self, hashtag):
        for tag in self.hashtags:
            if tag['text'] == hashtag:
                temp = self.text[tag['indices'][1]:]
                if '#' in temp:
                    temp = temp[:temp.index('#')]
                return temp