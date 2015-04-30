'''
__author__ = 'cobos'
'''
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json

class Media:
    def __init__(self, type_media, url,  content_type=None):
        self.type_media = type_media
        self.url = url

class Oauth:
    def __init__(self, oauth):
        self.oauth = oauth

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "10JkkyZKyUIWhZZ2XGAAsVMVE"
CONSUMER_SECRET = "GYCUogaCjDdE5vdIDpUIb5HBt9wni6aGgjFXBs9K0bXUfK6mln"

OAUTH_TOKEN = "394287364-gFJM5xPWtM4AgXMncGFVmQkNzyAW2OFt0QkZeNdq"
OAUTH_TOKEN_SECRET = "cLxvNv1MkEl31qD79xtdNmixwMJbfiVVep7vZ3OaHNcYT"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def get_trendy_topics(oauth):
    url = "https://api.twitter.com/1.1/trends/place.json?id=23424950"
    return requests.get(url=url, auth=oauth)

#returns a collection of the most recent tweets posted by th user
def get_tweets(oauth, user, count):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+user+"&count="+count+"&exclude_replies=true"
    return requests.get(url=url, auth=oauth)


def get_tweets_and_replies(oauth, user, count):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+user+"&count="+count
    return requests.get(url=url, auth=oauth)

#Following users id
def get_friends(oauth):
    url = "https://api.twitter.com/1.1/friends/ids.json"
    return requests.get(url=url, auth=oauth)

#Followrs users id
def get_followers(oauth):
    url = "https://api.twitter.com/1.1/followers/ids.json"
    return requests.get(url=url, auth=oauth)

def get_tweet_by_id(oauth, id):
    url = "https://api.twitter.com/1.1/show/user_timeline.json?id="+id
    return requests.get(url=url, auth=oauth)

def get_tweets_search(oauth, query, count):
    url = "https://api.twitter.com/1.1/search/tweets.json?q="+query+"&count="+count
    return requests.get(url=url, auth=oauth)

def get_user_information(oauth, screen_name):
    url = "https://api.twitter.com/1.1/users/show.json?screen_name="+screen_name
    return requests.get(url=url, auth=oauth)

def show_json_correct(data):
    data = json.loads(data.text)
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

#Make json object
def select_trendy_topics(data):
    json_data = json.loads(data.text)
    list=[]
    for dict in json_data:
        for item in dict[u'trends']:
            dict={}
            dict["name"] = unicode(item[u'name'])
            dict["query"] = unicode(item[u'query'])
            list.append(dict)
    return list

def select_search_tweets(data):
    json_data = json.loads(data.text)
    return json_data[u'statuses']

def load_json_object(data):
    data = json.loads(data.text)
    return data

def show_tweets(data):
    json_data = data
    i=0
    dict=[]
    if type(json_data) != type(dict):
        print "Error"
        return dict
    else:
        for item in json_data:
            print i
            twit_id = unicode(item[u'id_str'])
            user_id = unicode(item[u'user'][u'id_str'])
            name = unicode(item[u'user'][u'name'])
            screen_name = unicode(item[u'user'][u'screen_name'])
            time = unicode(item[u'created_at'])
            favorites = unicode(item[u'favorite_count'])
            retweets = unicode(item[u'retweet_count'])
            text = unicode(item[u'text'])
            twit={'twit_id': twit_id, 'name':name, 'time': time, 'text':text, 'screen_name': screen_name,
                  'user_id': user_id, 'favorites': favorites, 'retweets': retweets}
            dict.append(twit)
            i += 1
        return dict

def make_user_information(data):
    user={}
    if "errors" in data:
        return user
    user['created_at']=data['created_at']
    user['name']=data['name']
    user['description']=data['description']
    user['favourites_count']=data['favourites_count']
    user['followers_count']=data['followers_count']
    user['friends_count']=data['friends_count']
    user['created_at']=data['created_at']
    new_url = str(data['profile_image_url']).replace("_normal","_reasonably_small")
    user['profile_image_url']= new_url
    banner_url = str(data['profile_banner_url']) + "/1500x500"
    user['profile_banner_url'] = banner_url
    user['screen_name']=data['screen_name']
    return user

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print

