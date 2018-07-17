# Author : anbarief@live.com

import copy
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors as mplcolors
from .radial_bar import rbar
from . import adjustment as adjust
from . import functionals as func


class Tweets(list):

    """

    Tweets model.

    """

    def __init__(self, *args, filter_by_unique = False, **kwargs):

        if filter_by_unique:
            tweets = func.filter_unique(args[0])
        else:
            tweets = args[0]
            
        list.__init__(self, tweets, **kwargs)
        
    @property
    def sorted_by_time(self):
        return sorted(self, key = lambda x: x.created_at)

    @property
    def oldest(self):
        return self.sorted_by_time[0]

    @property
    def newest(self):
        return self.sorted_by_time[-1]

    
class Authors(object):

    """

    Authors model.

    """

    def __init__(self, tweets):

        self.tweets = tweets
        self.authors = {author.name : author for author in list(set([tweet.author for tweet in self.tweets]))}
        self.username = {author.screen_name : author for author in list(set([tweet.author for tweet in self.tweets]))}
        self.followers_count = {author: self.authors[author].followers_count for author in self.authors}
        self.following_count = {author: self.authors[author].friends_count for author in self.authors}
        self.totaltweets = {author: self.authors[author].statuses_count for author in self.authors}
        self.tweets_by_author = {author: [tweet for tweet in self.tweets if tweet.author.name == author] for author in self.authors}
        self.tweets_count = {author: len(self.tweets_by_author[author]) for author in self.tweets_by_author}

    def hbar_plot(self, ax, measurement = 'Followers', color = (0,0,1,1), incolor_measurement = None, height = 1, textsize = 7, **kwargs):

        measurements = {'Followers': self.followers_count, 'Following' : self.following_count, 'Total Tweets' : self.totaltweets, 'Sample Tweets' : self.tweets_count}
        sorted_authors = sorted(measurements[measurement], key = lambda x : measurements[measurement][x])

        if type(color) == str:
            color = mplcolors.hex2color(mplcolors.cnames[color])        
        
        colors = len(self.authors)*[color]
        if incolor_measurement != None:
            minor_max = max(measurements[incolor_measurement].values())
            transparency = [measurements[incolor_measurement][author]/minor_max for author in sorted_authors]
            colors = [(color[0], color[1], color[2], trans) for trans in transparency]

        var = [i+height for i in range(len(self.authors))]
        ax.barh([i-height/2 for i in var], [measurements[measurement][author] for author in sorted_authors], height = height, color = colors, **kwargs)
        ax.set_yticks(var)
        ax.set_yticklabels(sorted_authors, rotation = 'horizontal', size = textsize)

        if incolor_measurement != None:
            ax.set_xlabel(measurement + ' (color : '+incolor_measurement+')')
        else :
            ax.set_xlabel(measurement)
        plt.tight_layout()


class Splits(object):

    """

    Splits model.

    """

    def __init__(self, tweets):

        self.tweets = tweets
        self.texts = []
        for tweet in self.tweets:
            try:
                self.texts.append(tweet.full_text)
            except:
                self.texts.append(tweet.text)
        self.splits = func.split_texts(self.texts)
        
        self.splits_unique = list(set(self.splits))
        
        self.splits_freq = {}
        for split in self.splits_unique:
            self.splits_freq[split] = self.splits.count(split)
    
        self.sorted_splits_by_freq = sorted(self.splits_freq, key = lambda x: self.splits_freq[x])

        self.adjusted = None 

    def apply_adjustment(self, adjustment):
    
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

    def hbar_plot(self, ax, adjustment = None, color = (0, 0.6, 1, 1), incolor_rt = False, height = 0.5, textsize = 7, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']
        else:
            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if type(color) == str:
            color = mplcolors.hex2color(mplcolors.cnames[color])        

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.tweets, string_inclusion = split) for split in sorted_splits_by_freq]
            max_total_rts = max(sorted_total_rts)
            col = [(color[0], color[1], color[2], total_rt/max_total_rts) for total_rt in sorted_total_rts]
        else:
            col = color
        
        var = [i+height for i in range(len(splits_freq))]
        ax.barh([i-height/2 for i in var], [splits_freq[split] for split in sorted_splits_by_freq], height = height, color = col, **kwargs)
        ax.set_yticks(var)
        ax.set_yticklabels(sorted_splits_by_freq, rotation = 'horizontal')

        default_summary = "split \'"+sorted_splits_by_freq[0]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[0]])+\
                  " times, and split \'"+sorted_splits_by_freq[-1]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[-1]])+' times.'
        if incolor_rt:
            idx = sorted_total_rts.index(max_total_rts)
            default_summary += "\n\n split \'"+sorted_splits_by_freq[idx]+"\' involved with "+str(max_total_rts)+" RTs."
            
        ax.set_title(default_summary, size = textsize)
        plt.tight_layout()

    def rbar_plot(self, ax, adjustment = None, base_radius = 50, bar_width = 6, color = (0, 0, 1, 1), incolor_rt = False, textsize = 7):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']
        else:
            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if type(color) == str:
            color = mplcolors.hex2color(mplcolors.cnames[color])        

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.tweets, string_inclusion = split) for split in sorted_splits_by_freq]
            max_total_rts = max(sorted_total_rts)
            colors = [(color[0]*total_rt/max_total_rts, color[1]*total_rt/max_total_rts, color[2]*total_rt/max_total_rts, 1) for total_rt in sorted_total_rts]
        else:
            colors = [color]*len(splits_freq)

        rbar(ax, list(range(len(splits_freq))), \
                  [splits_freq[sorted_splits_by_freq[index]] for index in range(len(splits_freq))], \
                  base_radius, col = colors, \
                  label = sorted_splits_by_freq, bar_width = bar_width, textsize = textsize)

        default_summary = "split \'"+sorted_splits_by_freq[0]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[0]])+\
                  " times, and split \'"+sorted_splits_by_freq[-1]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[-1]])+' times.'
        if incolor_rt:
            idx = sorted_total_rts.index(max_total_rts)
            default_summary += "\n\n split \'"+sorted_splits_by_freq[idx]+"\' involved with "+str(max_total_rts)+" RTs."
        
        ax.set_title(default_summary, size = textsize)
        ax.tick_params(colors=(0,0,0,0))
        plt.tight_layout()


class Hashtags(object):

    """

    Hashtags model.

    """

    def __init__(self, tweets):

        self.tweets = tweets
    
        texts = []
        for tweet in self.tweets:
            try:
                texts.append(tweet.full_text)
            except:
                texts.append(tweet.text)
        hashtags = func.split_texts(texts)

        self.hashtags = [hashtag for hashtag in hashtags if len(hashtag) > 1 and hashtag[0] == '#' and hashtag[1] != '#']
        
        self.hashtags_unique = list(set(self.hashtags))
        
        self.hashtags_freq = {}
        for hashtag in self.hashtags_unique:
            self.hashtags_freq[hashtag] = self.hashtags.count(hashtag)
    
        self.sorted_hashtags_by_freq = sorted(self.hashtags_freq, key = lambda x: self.hashtags_freq[x])

        self.adjusted = None

    def apply_adjustment(self, adjustment):

        self.adjusted = {'hashtags_freq': copy.deepcopy(self.hashtags_freq)}

        exclude = []
        if adjustment.exclude != None:
            exclude = adjustment.exclude
        
        if adjustment.freq_lim != None:
            minmax = adjustment.freq_lim           
            for hashtag in self.hashtags_freq:
                if (hashtag in exclude) or not (minmax[0] <= self.hashtags_freq[hashtag] <= minmax[1]):
                    del(self.adjusted['hashtags_freq'][hashtag])
    
        if adjustment.char_lim != None:
            minmax = adjustment.char_lim
            for hashtag in copy.deepcopy(self.adjusted['hashtags_freq']):
                if (hashtag in exclude) or not (minmax[0] <= len(hashtag) <= minmax[1]):
                    del(self.adjusted['hashtags_freq'][hashtag])

        self.adjusted['sorted_hashtags_by_freq'] = sorted(self.adjusted['hashtags_freq'], key = lambda x: self.adjusted['hashtags_freq'][x])
        
        return self.adjusted

    def hbar_plot(self, ax, adjustment = None, color = (0, 0.6, 1, 1), incolor_rt = False, height = 0.5, textsize = 7, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            hashtags_freq = self.adjusted['hashtags_freq']
            sorted_hashtags_by_freq = self.adjusted['sorted_hashtags_by_freq']
        else:
            hashtags_freq = self.hashtags_freq
            sorted_hashtags_by_freq = self.sorted_hashtags_by_freq

        if type(color) == str:
            color = mplcolors.hex2color(mplcolors.cnames[color])        

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.tweets, string_inclusion = hashtag) for hashtag in sorted_hashtags_by_freq]
            max_total_rts = max(sorted_total_rts)
            col = [(color[0], color[1], color[2], total_rt/max_total_rts) for total_rt in sorted_total_rts]
        else:
            col = color
        
        var = [i+height for i in range(len(hashtags_freq))]
        ax.barh([i-height/2 for i in var], [hashtags_freq[hashtag] for hashtag in sorted_hashtags_by_freq], height = height, color = col, **kwargs)
        ax.set_yticks(var)
        ax.set_yticklabels(sorted_hashtags_by_freq, rotation = 'horizontal')

        default_summary = "hashtag \'"+sorted_hashtags_by_freq[0]+"\' appeared "+str(hashtags_freq[sorted_hashtags_by_freq[0]])+\
                  " times, and hashtag \'"+sorted_hashtags_by_freq[-1]+"\' appeared "+str(hashtags_freq[sorted_hashtags_by_freq[-1]])+' times.'
        if incolor_rt:
            idx = sorted_total_rts.index(max_total_rts)
            default_summary += "\n\n hashtag \'"+sorted_hashtags_by_freq[idx]+"\' involved with "+str(max_total_rts)+" RTs."
            
        ax.set_title(default_summary, size = textsize)
        plt.tight_layout()

    def rbar_plot(self, ax, adjustment = None, base_radius = 50, bar_width = 6, color = (0, 0, 1, 1), incolor_rt = False, textsize = 7):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            hashtags_freq = self.adjusted['hashtags_freq']
            sorted_hashtags_by_freq = self.adjusted['sorted_hashtags_by_freq']
        else:
            hashtags_freq = self.hashtags_freq
            sorted_hashtags_by_freq = self.sorted_hashtags_by_freq

        if type(color) == str:
            color = mplcolors.hex2color(mplcolors.cnames[color])        

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.tweets, string_inclusion = hashtag) for hashtag in sorted_hashtags_by_freq]
            max_total_rts = max(sorted_total_rts)
            colors = [(color[0]*total_rt/max_total_rts, color[1]*total_rt/max_total_rts, color[2]*total_rt/max_total_rts, 1) for total_rt in sorted_total_rts]
        else:
            colors = [color]*len(hashtags_freq)

        rbar(ax, list(range(len(hashtags_freq))), \
                  [hashtags_freq[sorted_hashtags_by_freq[index]] for index in range(len(hashtags_freq))], \
                  base_radius, col = colors, \
                  label = sorted_hashtags_by_freq, bar_width = bar_width, textsize = textsize)

        default_summary = "hashtag \'"+sorted_hashtags_by_freq[0]+"\' appeared "+str(hashtags_freq[sorted_hashtags_by_freq[0]])+\
                  " times, and hashtag \'"+sorted_hashtags_by_freq[-1]+"\' appeared "+str(hashtags_freq[sorted_hashtags_by_freq[-1]])+' times.'
        if incolor_rt:
            idx = sorted_total_rts.index(max_total_rts)
            default_summary += "\n\n hashtag \'"+sorted_hashtags_by_freq[idx]+"\' involved with "+str(max_total_rts)+" RTs."
        
        ax.set_title(default_summary, size = textsize)
        ax.tick_params(colors=(0,0,0,0))
        plt.tight_layout()
