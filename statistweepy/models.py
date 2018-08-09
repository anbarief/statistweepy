# Author : anbarief@live.com
import itertools
import pytz
import copy
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors as mplcolors
import operator
from statistweepy import radial_bar
from statistweepy import utils
rbar_A = radial_bar.rbar_A
rbar_B = radial_bar.rbar_B


class Adjustment(object):

    """
    This object is only useful for \'models.Splits\' model. The Adjusment object stores information of different type of adjustments proposed by the analyst.\n
    Current adjustments : frequency limits, character limits, and exclude container which should contain splits to be neglected.
    """

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
    
    def __init__(self, tweets, repr_mode = 'texts'):

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
            raise TypeError('tweets must be of statistweepy.models.Status object')

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
    def sorted_by_time(self):
        return sorted(self, key=operator.attrgetter('created_at'))

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

    def filter_by_time_interval(self, interval):

        filtered = Tweets(filter(lambda x: interval[0] <= x.created_at <= interval[1], self))

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

    def _time_distribution(self, unit = 'hour', output = 'frequency', cont_hist = False):

        if not any([unit == 'year', unit == 'month', unit == 'day', unit == 'hour']):
            raise AssertionError(' The argument unit must be one of \'year\',  \'month\',  \'day\', or \'hour\'. ')
            
        unicity_key = operator.attrgetter('created_at.'+unit)
        tweets = sorted(self, key=unicity_key)
        distribution = {}

        for time, time_tweets in itertools.groupby(tweets, key=unicity_key):

            time_tweets = list(time_tweets)
            
            if output == 'frequency':
                
                distribution[time] = len(time_tweets)
                fy = lambda x: x

            elif output == 'tweets':

                distribution[time] = time_tweets
                fy = lambda x: len(x)

            else:

                raise AssertionError(' The argument output must be either \'frequency\', or \'tweets\'. ')

        if cont_hist:

            axes = cont_hist[0]

            if unit == 'year':
                
                xt = [tweet.created_at.year + (tweet.created_at.month + (tweet.created_at.day + tweet.created_at.hour/24)/31)/12 \
                          for tweet in self]

                a = int(min(xt))
                b = int(max(xt))
                ticks = range(a-1, b+2)

            elif unit == 'month':
                
                xt = [(tweet.created_at.month + (tweet.created_at.day + tweet.created_at.hour/24)/31) \
                          for tweet in self]

                ticks = range(1, 13)

            elif unit == 'day':
                
                xt = [(tweet.created_at.day + tweet.created_at.hour/24) \
                          for tweet in self]

                ticks = range(1, 32)

            elif unit == 'hour':

                xt = [tweet.created_at.hour + (tweet.created_at.minute + tweet.created_at.second/60)/60 \
                          for tweet in self]
                
                ticks = range(0, 25)

            histogram = axes.hist(xt, **cont_hist[1])
            axes.set_xticks(ticks)
            axes.set_xticklabels([str(i) for i in ticks])
            axes.set_xlabel(unit)
            axes.set_ylabel('frequency')
            
            return distribution, histogram

        return distribution

   
class Authors(object):

    """
    Authors model for insights on the authors of the tweets.\n
    self.authors_tweets : a dictionary with keys of unique authors, each gives value of a list containing the author\'s tweets.\n
    self.followers_count : a dictionary with keys of unique authors, each gives the number of followers of the account.\n
    self.following_count : a dictionary with keys of unique authors, each gives the number of friends of the account.\n
    self.total_tweets : a dictionary with keys of unique authors, each gives the number of total tweets sent from the account.\n
    self.sample_count : a dictionary with keys of unique authors, each gives the number of tweets appeared in the sample.\n
    """

    def __init__(self, tweets):

        if not isinstance(tweets, Tweets):
            raise TypeError('tweets must be a Tweets object')

        unicity_key = operator.attrgetter('author.screen_name')
        tweets = sorted(tweets, key=unicity_key)
        self._tweets = tweets
        self.authors_tweets = {}
        self.followers_count = {}
        self.following_count = {}
        self.total_tweets = {}
        self.likes_count = {}
        self.sample_count = {}
        
        for screen_name, author_tweets in itertools.groupby(tweets, key=unicity_key):
            
            author_tweets = list(author_tweets)
            author = author_tweets[0].author

            self.authors_tweets[screen_name] = (author.name, Tweets(author_tweets))
            self.followers_count[screen_name] = author.followers_count
            self.following_count[screen_name] = author.friends_count
            self.total_tweets[screen_name] = author.statuses_count
            self.likes_count[screen_name] = author.favourites_count
            self.sample_count[screen_name] = len(author_tweets)


    def hbar_plot(self, ax, measurement = 'Followers', color = (0,0,1,1), incolor_measurement = None, width = 1, space = True, text_size = 7):

        """
        This method gives a horizontal bar plot of a measurement : followers count, friend count, total tweets, and sample tweets count.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.
        """

        measurements = {'Followers': self.followers_count, \
                        'Following' : self.following_count, \
                        'Total Tweets' : self.total_tweets, \
                        'Sample Tweets' : self.sample_count}

        sorted_authors = sorted(measurements[measurement], key = lambda x : measurements[measurement][x])

        if isinstance(color, str):
            
            color = mplcolors.hex2color(mplcolors.cnames[color])        
        
        colors = len(self.authors_tweets)*[color]
        if incolor_measurement != None:
            
            minor_max = max(measurements[incolor_measurement].values())
            transparency = [measurements[incolor_measurement][author]/minor_max for author in sorted_authors]
            colors = [(color[0], color[1], color[2], trans) for trans in transparency]

        if space:
            space = width
        else:
            space = 0

        var = ( 1 +  i*(space + width)  for i in range(len(self.authors_tweets)) )

        bar_pos = []; ytick_pos = []

        for i in var:

            bar_pos.append(i - width/2) 
            ytick_pos.append(i)
        
        ax.barh(bar_pos, [measurements[measurement][author] for author in sorted_authors], height = width, color = colors)
        ax.set_yticks(ytick_pos)
        ax.set_yticklabels(sorted_authors, rotation = 'horizontal', size = text_size)

        ax.set_ylim([1 - width/2 - space, max(ytick_pos) + width/2 + space])

        if incolor_measurement != None:
            
            ax.set_xlabel(measurement + ' (color : '+incolor_measurement+')')

        else :

            ax.set_xlabel(measurement)

        plt.tight_layout()


class Splits(object):

    """
    Splits model for approximating words distribution on the sample (tweets). \
    The approximation is based on list.split() method.\n
    self.splits_unique : a set containing all unique splits from the tweets
    self.splits_freq : a dictionary of splits frequency
    self.sorted_splits_by_freq : a list of sorted splits by frequency
    """

    def __init__(self, tweets):

        if not isinstance(tweets, Tweets):
            raise TypeError('tweets must be a Tweets object')
        
        self.tweets = tweets
        self.texts = []
        for tweet in self.tweets:

            try:
                self.texts.append(tweet.full_text)
            except:
                self.texts.append(tweet.text)

        self._texts_split = utils.split_texts(self.texts)

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

    def hbar_plot(self, ax, adjustment = None, color = (0, 0.6, 1, 1), incolor_rt = False, width = 1, space = True, text_size = 7):

        """
        This method gives a horizontal bar plot of the splits frequency.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.\n    
        """
        
        if adjustment != None:
            
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']

        else:

            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if isinstance(color, str):

            color = mplcolors.hex2color(mplcolors.cnames[color])        

        if incolor_rt:

            sorted_total_rts = [utils.total_rts(self.tweets, string_inclusion = split) for split in sorted_splits_by_freq]
            max_total_rts = max(sorted_total_rts)
            col = [(color[0], color[1], color[2], total_rt/max_total_rts) for total_rt in sorted_total_rts]

        else:

            col = color

        if space:

            space = width

        else:

            space = 0

        var = ( 1 +  i*(space + width)  for i in range(len(splits_freq)) )

        bar_pos = []; ytick_pos = []

        for i in var:

            bar_pos.append(i - width/2)
            ytick_pos.append(i)
         
        ax.barh(bar_pos, [splits_freq[split] for split in sorted_splits_by_freq], height = width, color = col)

        ax.set_yticks(ytick_pos)
        ax.set_yticklabels(sorted_splits_by_freq, rotation = 'horizontal', size = text_size)
        ax.set_ylim([1 - width/2 - space, max(ytick_pos) + width/2 + space])

        if incolor_rt:
            
            ax.set_xlabel('Splits frequency count. (color : total RTs)')

        else :

            ax.set_xlabel('Splits frequency count.')
            
        plt.tight_layout()

    def rbar_plot(self, ax, mode = 'A', adjustment = None, base_radius = 50, bar_width = 6, color = (0, 0, 1, 1), text_size = 7):

        """
        This method gives a radial bar plot of the splits frequency.\n
        The first required argument is \'ax\' which should be an object of \'matplotlib.axes._subplots.AxesSubplot\'.\n
        The \'mode\' should be either \'A\' or \'B\', which gives different version of the radial bar plot.
        """
        
        if adjustment != None:
            
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']

        else:

            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if isinstance(color, str):

            color = mplcolors.hex2color(mplcolors.cnames[color])        

        colors = [color]*len(splits_freq)

        if mode == 'A':
            
            rbar_A(ax, [splits_freq[sorted_splits_by_freq[index]] for index in range(len(splits_freq))], \
                      base_radius, col = colors, \
                      label = sorted_splits_by_freq, bar_width = bar_width, text_size = text_size)

        if mode == 'B':

            rbar_B(ax, [splits_freq[sorted_splits_by_freq[index]] for index in range(len(splits_freq))], \
                      base_radius, col = colors, \
                      label = sorted_splits_by_freq, bar_width = bar_width, text_size = text_size)
            
        ax.tick_params(colors=(0,0,0,0))

        ax.set_xlabel('Splits frequency count.')
        
        plt.tight_layout()
