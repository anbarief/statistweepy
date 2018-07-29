# Author : anbarief@live.com

import itertools
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

    def __init__(self, tweets, **kwargs):

        tweets = utils.filter_unique(tweets)

        super().__init__(tweets, **kwargs)
        
    def __repr__(self):

        try:
            head = self[0].text
        except:
            head = self[0].full_text

        if len(self) > 1:

            try:
                tail = self[-1].text
            except:
                tail = self[-1].full_text

            return '[0]: ' + head + '\n.'*3 + '\n[{}]: '.format(len(self)-1) + tail

        else:

            return '[0]: ' + head

    @property
    def sorted_by_time(self):
        return sorted(self, key=operator.attrgetter('created_at'))

    @property
    def oldest(self):
        return min(self, key=operator.attrgetter('created_at'))

    @property
    def newest(self):
        return max(self, key=operator.attrgetter('created_at'))

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

    def time_distribution(self, unit = 'hour', output = 'frequency'):

        if not any([unit == 'year', unit == 'month', unit == 'day', unit == 'hour', unit == 'minute', unit == 'continuous']):
            raise AssertionError(' The argument unit must be one of \'year\',  \'month\',  \'day\',  \'hour\',  \'minute\', or \'continuous\'. ')
        
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
        self.authors_tweets = {}
        self.followers_count = {}
        self.following_count = {}
        self.total_tweets = {}
        self.sample_count = {}
        
        for screen_name, author_tweets in itertools.groupby(tweets, key=unicity_key):
            
            author_tweets = list(author_tweets)
            author = author_tweets[0].author

            self.authors_tweets[screen_name] = (author.name, author_tweets)
            self.followers_count[screen_name] = author.followers_count
            self.following_count[screen_name] = author.friends_count
            self.total_tweets[screen_name] = author.statuses_count
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

        if incolor_rt != None:
            
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
