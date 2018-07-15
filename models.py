# Author : anbarief@live.com

import copy
import numpy
import matplotlib.pyplot as plt
from statistweepy.radial_bar import rbar
import statistweepy.adjustment as adjust
import statistweepy.functionals as func


class Authors(object):

    def __init__(self, tweet_stats_list, filter_unique = False):

        if filter_unique:
            self.stats = func.filter_unique(tweet_stats_list)
        else:
            self.stats = tweet_stats_list
        self.oldest = min([tweet.created_at for tweet in self.stats])
        self.newest = max([tweet.created_at for tweet in self.stats])
        self.authors = {author.name : author for author in list(set([tweet.author for tweet in self.stats]))}
        self.username = {author.screen_name : author for author in list(set([tweet.author for tweet in self.stats]))}
        self.followers_count = {author: self.authors[author].followers_count for author in self.authors}
        self.following_count = {author: self.authors[author].friends_count for author in self.authors}
        self.totaltweets = {author: self.authors[author].statuses_count for author in self.authors}
        self.stats = {author: [stat for stat in self.stats if stat.author.name == author] for author in self.authors}
        self.stats_count = {author: len(self.stats[author]) for author in self.stats}

    def hbar_plot(self, ax, measurement = 'Total Tweets', incolor_measurement = None, width = 1, textsize = 7, color = (0, 0.5, 1, 1), **kwargs):

        measurements = {'Followers': self.followers_count, 'Following' : self.following_count, 'Total Tweets' : self.totaltweets, 'Sample Tweets' : self.stats_count}
        sorted_authors = sorted(measurements[measurement], key = lambda x : measurements[measurement][x])
        colors = len(self.authors)*[color]
        if incolor_measurement != None:
            minor_max = max(measurements[incolor_measurement].values())
            transparency = [measurements[incolor_measurement][author]/minor_max for author in sorted_authors]
            colors = [(color[0], color[1], color[2], trans) for trans in transparency]
        var = [i+width for i in range(len(self.authors))]
        ax.barh([i-width/2 for i in var], [measurements[measurement][author] for author in sorted_authors], height = width, color = colors)
        ax.set_yticks(var)
        ax.set_yticklabels(sorted_authors, rotation = 'horizontal', size = textsize)

        if incolor_measurement != None:
            ax.set_xlabel(measurement + ' (color : '+incolor_measurement+')')
        else :
            ax.set_xlabel(measurement)
        plt.tight_layout()


class Splits(object):

    def __init__(self, tweet_stats_list, filter_unique = False):

        if filter_unique:
            self.stats = func.filter_unique(tweet_stats_list)
        else:
            self.stats = tweet_stats_list
        self.oldest = min([tweet.created_at for tweet in self.stats])
        self.newest = max([tweet.created_at for tweet in self.stats])
        self.texts = []
        for tweet in self.stats:
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

    def hbar_plot(self, ax, title = '', adjustment = None, color = (0, 0.6, 1, 1), textsize = 7, incolor_rt = False, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']
        else:
            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.stats, string_inclusion = split) for split in sorted_splits_by_freq]
            max_total_rts = max(sorted_total_rts)
            col = [(color[0], color[1], color[2], total_rt/max_total_rts) for total_rt in sorted_total_rts]
        else:
            col = color
        
        var = [i+2 for i in range(len(splits_freq))]
        w = 1
        ax.barh([i-w/2 for i in var], [splits_freq[split] for split in sorted_splits_by_freq], color = col)
        ax.set_yticks(var)
        ax.set_yticklabels(sorted_splits_by_freq, rotation = 'horizontal')

        default_summary = "split \'"+sorted_splits_by_freq[0]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[0]])+\
                  " times, and split \'"+sorted_splits_by_freq[-1]+"\' appeared "+str(splits_freq[sorted_splits_by_freq[-1]])+' times.'
        if incolor_rt:
            idx = sorted_total_rts.index(max_total_rts)
            default_summary += "\n\n split \'"+sorted_splits_by_freq[idx]+"\' involved with "+str(max_total_rts)+" RTs."
        if title == '':
            title = default_summary
            
        ax.set_title(title, size = textsize)
        plt.tight_layout()

    def rbar_plot(self, ax, title = '', adjustment = None, color = (0, 0.6, 1, 1), base_radius = 50, bar_width = 6, textsize = 7, incolor_rt = False, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            splits_freq = self.adjusted['splits_freq']
            sorted_splits_by_freq = self.adjusted['sorted_splits_by_freq']
        else:
            splits_freq = self.splits_freq
            sorted_splits_by_freq = self.sorted_splits_by_freq

        if len(sorted_splits_by_freq) == 0:
            raise AssertionError()
            return None

        if incolor_rt:
            sorted_total_rts = [func.total_rts(self.stats, string_inclusion = split) for split in sorted_splits_by_freq]
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
        if title == '':
            title = default_summary
            
        ax.set_title(title, size = textsize)
        ax.tick_params(colors=(0,0,0,0))
        plt.tight_layout()
