# Author: anbarief@live.com

import tweepy
from tweepy import OAuthHandler
from statistweepy import models
import numpy
import datetime


class Authentication(object):

    __slots__ = ('consumer_key', 'consumer_secret', 'access_token', 'access_secret', \
                 'auth', 'api')

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth)


class Collection(object):

    __slots__ = ('auth_object', 'api', 'collection', 'collection_time')

    def __init__(self, auth_object):

        self.auth_object = auth_object
        self.api = self.auth_object.api
        self.collection = None

    def collect_home(self, method = 'Default', n = 20, **kwargs):

        if method == 'Default':

            public_stats = self.api.home_timeline()

        if method == 'Cursor':
            
            public_stats = tweepy.Cursor(self.api.home_timeline, **kwargs).items(n)
        
        stats = [stat for stat in public_stats]

        self.collection_time = datetime.datetime.now();
        self.collection = models.Tweets(stats)

    def collect_user(self, username, n = 20, **kwargs):

        user_stats = tweepy.Cursor(self.api.user_timeline, \
                                   screen_name = username, **kwargs).items(n)

        stats = [stat for stat in user_stats]

        self.collection_time = datetime.datetime.now();
        self.collection = models.Tweets(stats)

    @staticmethod
    def save(*args, **kwargs):
        numpy.save(*args, **kwargs)

    @staticmethod
    def load(filename):
        return numpy.load(filename)
