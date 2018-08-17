# Author : anbarief@live.com
import itertools
import pytz
import copy
import numpy
import operator
import tweepy
from statistweepy import utils
from statistweepy import viz


class Adjustment(object):

    """
    This object is only useful for \'models.Splits\' model. The Adjusment object stores information of different type of adjustments proposed by the analyst.\n
    Current adjustments : frequency limits, character limits, and exclude container which should contain splits to be neglected.
    """

    __slots__ = ('title', 'freq_lim', 'char_lim', 'exclude')

    def __init__(self, title = "an adjustment.", **kwargs):

        self.title = title

        if 'freq_lim' in kwargs:
            self.freq_lim = kwargs['freq_lim']
        else:
            self.freq_lim = None

        if 'char_lim' in kwargs:
            self.char_lim = kwargs['char_lim']
        else:
            self.char_lim = None

        if 'exclude' in kwargs:
            self.exclude = kwargs['exclude']
        else:
            self.exclude = None

            
class Tweets(list):

    """
    Tweets model is a list-like object containing \'tweepy.models.Status\' objects.
    """
    
    def __init__(self, tweets):

        tweets = utils.filter_unique(tweets)
        
        super().__init__(tweets)

    def __repr__(self):

        head = self[0].author.screen_name
            
        if len(self) > 1:

            tail = self[-1].author.screen_name

            return '[[0]: by @' + head + ', ...... , ' + '[{}]: by @'.format(len(self)-1) + tail + ']'
        
        else:

            return '[[0]: by @' + head + ']'

    def append(self, tweet):

        if not isinstance(tweet, self[0].__class__):
            raise TypeError('tweet must be of tweepy.models.Status object')

        super().append(tweet)

    def extend(self, tweets):

        if not isinstance(tweets, Tweets):
            raise TypeError('tweets must be of statistweepy.models.Tweets object')

        super().extend(tweets)

    def insert(self, index, tweet):

        if not isinstance(tweet, self[0].__class__):
            raise TypeError('tweet must be of tweepy.models.Status object')

        super().insert(index, tweet)

    def sort(self, by = 'time', reverse = False):

        if by == 'time':
            
            in_key = operator.attrgetter('created_at')

        elif by == 'retweet_count':

            in_key = operator.attrgetter(by)

        elif by == 'favorite_count':

            in_key = operator.attrgetter(by)

        elif by == 'username':

            in_key = operator.attrgetter('author.screen_name')

        elif by == 'length':

            try:
                in_key = lambda x: len(x.text)
            except:
                in_key = lambda x: len(x.full_text)
        
        super().sort(key = in_key, reverse = reverse)

    @property
    def oldest(self):
        return min(self, key=operator.attrgetter('created_at'))

    @property
    def newest(self):
        return max(self, key=operator.attrgetter('created_at'))

    def authors(self):

        unicity_key = operator.attrgetter('author.screen_name')
        tweets = sorted(self, key = unicity_key)

        authors = {}

        for screen_name, author_tweets in itertools.groupby(tweets, key=unicity_key):
            
            author_tweets = list(author_tweets)
            author = author_tweets[0].author

            authors[screen_name] = (author.name, Tweets(author_tweets))

        return authors

    def view(self, start, end, attr = 'text'):

        viewed = ''
        index = start
        attr_dict = {'retweet_count' : 'retweet_count', \
                     'favorite_count' : 'favorite_count', \
                     'language' : 'lang', \
                     'time' : 'created_at'}
        
        for tweet in self[start:end+1]:

            if attr == 'text':

                try:
                    new = tweet.text.encode()

                except:
                    new = tweet.full_text.encode()

            else:

                new = getattr(tweet, attr_dict[attr])

            viewed += '[{}] by @{} : {}\n'.format(index, tweet.author.screen_name, new)
            index += 1
    
        print(viewed)

    def filter_by_username(self, username):

        filtered = Tweets(filter(lambda x: x.author.screen_name == username, self))

        try:
            filtered.__repr__()
        except:
            return None
            
        return filtered

    def filter_by_name(self, name):

        filtered = Tweets(filter(lambda x: x.author.name == name, self))

        try:
            filtered.__repr__()
        except:
            return None
        
        return filtered

    def filter_by_time_interval(self, oldest, newest):

        filtered = Tweets(filter(lambda x: oldest <= x.created_at <= newest, self))

        try:
            filtered.__repr__()
        except:
            return None
        
        return filtered

    def filter_by_retweet_count(self, min_rts, max_rts):

        filtered = Tweets(filter(lambda x: min_rts <= x.retweet_count <= max_rts, self))

        try:
            filtered.__repr__()
        except:
            return None
        
        return filtered

    def filter_by_favorite_count(self, min_likes, max_likes):

        filtered = Tweets(filter(lambda x: min_likes <= x.favorite_count <= max_rt, self))

        try:
            filtered.__repr__()
        except:
            return None
        
        return filtered

    def apply_timezone(self, timezone = 'Singapore'):
        
        for tweet in self:

            time = tweet.created_at
            
            if time.tzinfo is None:
                time = time.replace(tzinfo = pytz.utc)

            tz = pytz.timezone(timezone)
            tweet.created_at = time.astimezone(tz)

 
class Authors(object):

    """
    Authors model for insights on the authors of the tweets.\n
    self.authors_tweets : a dictionary with keys of unique authors, each gives value of a list containing the author\'s tweets.\n
    self.followers_count : a dictionary with keys of unique authors, each gives the number of followers of the account.\n
    self.following_count : a dictionary with keys of unique authors, each gives the number of friends of the account.\n
    self.total_tweets : a dictionary with keys of unique authors, each gives the number of total tweets sent from the account.\n
    self.sample_count : a dictionary with keys of unique authors, each gives the number of tweets appeared in the sample.\n
    """

    __slots__ = ('_tweets', 'authors_tweets', 'followers_count', 'following_count', 'total_tweets', \
                 'total_likes', 'sample_count')

    def __init__(self, tweets):

        if not isinstance(tweets, Tweets):
            raise TypeError("tweets must be a statistweepy.models.Tweets object.")

        unicity_key = operator.attrgetter('author.screen_name')
        tweets = sorted(tweets, key=unicity_key)
        self._tweets = tweets
        self.authors_tweets = {}
        self.followers_count = {}
        self.following_count = {}
        self.total_tweets = {}
        self.total_likes = {}
        self.sample_count = {}
        
        for screen_name, author_tweets in itertools.groupby(tweets, key=unicity_key):
            
            author_tweets = list(author_tweets)
            author = author_tweets[0].author

            self.authors_tweets[screen_name] = (author.name, Tweets(author_tweets))
            self.followers_count[screen_name] = author.followers_count
            self.following_count[screen_name] = author.friends_count
            self.total_tweets[screen_name] = author.statuses_count
            self.total_likes[screen_name] = author.favourites_count
            self.sample_count[screen_name] = len(author_tweets)

    def hbar_plot(self, ax, meas = 'followers_count', **kwargs):

        """
        This method gives a horizontal bar plot of a measurement : followers count, friend count, total tweets, and sample tweets count.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.
        """

        viz.hbar_plot_Authors(self, ax, meas = meas, **kwargs)

    def hbar2sided_plot(self, ax, meas_left = 'followers_count', meas_right = 'following_count', colors = ['red', 'blue'], **kwargs):

        """
        This method gives a horizontal bar plot of a measurement : followers count, friend count, total tweets, and sample tweets count.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.
        """

        viz.hbar2sided_plot_Authors(self, ax, meas_left = meas_left, meas_right = meas_right, colors = colors, **kwargs)

    def scatter_plot(self, ax, meas_x = 'followers_count', meas_y = 'following_count', **kwargs):

        viz.scatter_plot_Authors(self, ax, meas_x=meas_x, meas_y=meas_y, **kwargs)


class Splits(object):

    """
    Splits model for approximating words distribution on the sample (tweets). \
    The approximation is based on list.split() method.\n
    self.splits_unique : a set containing all unique splits from the tweets
    self.splits_freq : a dictionary of splits frequency
    self.sorted_splits_by_freq : a list of sorted splits by frequency
    """

    __slots__ = ('tweets', 'texts', '_texts_split', 'splits', 'splits_unique', 'splits_freq', \
                 'sorted_splits_by_freq', 'adjusted', 'naive')

    def __init__(self, tweets, naive = True):

        if not isinstance(tweets, Tweets):
            raise TypeError("tweets must be a statistweepy.models.Tweets object.")

        self.naive = naive
        self.tweets = tweets
        self.texts = []
        for tweet in self.tweets:

            try:
                self.texts.append(tweet.full_text)
            except:
                self.texts.append(tweet.text)

        self._texts_split = utils.split_texts(self.texts, naive)

        self.splits = []
        for i in self._texts_split:

            self.splits.extend(i)

        self.splits_unique = set(self.splits)
        self.splits_freq = {split : self.splits.count(split) for split in self.splits_unique}
        self.sorted_splits_by_freq = sorted(self.splits_freq, key = lambda x: self.splits_freq[x])

        self.adjusted = None 

    def apply_adjustment(self, adjustment):

        """
        This method returns a dictionary with keys : \'splits_freq\', and \'sorted_splits_by_freq\'.\n
        The first gives a dictionary of splits frequency, filtered by the adjustment argument.\n
        The latter gives a list of all the corresponding splits, sorted by frequency. 
        """
    
        self.adjusted = {'splits_freq': copy.deepcopy(self.splits_freq)}

        exclude = []
        
        if adjustment.exclude != None:

            exclude = adjustment.exclude
        
        if adjustment.freq_lim != None:

            minmax = adjustment.freq_lim           

            for split in self.splits_freq:

                if (split in exclude) or not (minmax[0] <= self.splits_freq[split] <= minmax[1]):

                    del(self.adjusted['splits_freq'][split])
    
        if adjustment.char_lim != None:

            minmax = adjustment.char_lim

            for split in copy.deepcopy(self.adjusted['splits_freq']):

                if (split in exclude) or not (minmax[0] <= len(split) <= minmax[1]):

                    del(self.adjusted['splits_freq'][split])

        self.adjusted['sorted_splits_by_freq'] = sorted(self.adjusted['splits_freq'], key = lambda x: self.adjusted['splits_freq'][x])
        
        return self.adjusted

    def hbar_plot(self, ax, adjustment = None, **kwargs):

        """
        This method gives a horizontal bar plot of the splits frequency.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.\n    
        """

        viz.hbar_plot_Splits(self, ax, adjustment = adjustment, **kwargs)

    def rbar_plot(self, ax, adjustment = None, **kwargs):

        """
        This method gives a radial bar plot of the splits frequency.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.\n
        The \'mode\' should be either \'A\' or \'B\', which gives different version of the radial bar plot.
        """
        
        viz.rbar_plot_Splits(self, ax, adjustment = adjustment, **kwargs)
