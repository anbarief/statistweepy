# Author : anbarief@live.com

import copy
import numpy
import matplotlib.pyplot as plt
import statistweepy.circular_bar as cbar
import statistweepy.adjustment as adjust
import statistweepy.functionals as func


class HighLevelSummary(object):

    def __init__(self, tweet_stats_list):

        self.stats = func.filter_unique(tweet_stats_list)
        self.len = len(self.stats)
        self.oldest = min([tweet.created_at for tweet in self.stats])
        self.newest = max([tweet.created_at for tweet in self.stats])
        self.authors = set([tweet.author.name for tweet in self.stats])


class Words(object):

    def __init__(self, tweet_stats_list):

        self.high_level_summary = HighLevelSummary(tweet_stats_list)
        self.stats = self.high_level_summary.stats 
        self.texts = []
        for tweet in self.stats:
            self.texts.append(tweet.text)
        self.words = func.texts_to_words(self.texts)
        
        self.words_unique = set(self.words)
        
        self.words_freq = {}
        for word in self.words_unique:
            self.words_freq[word] = self.words.count(word)
    
        self.sorted_words_by_freq = sorted(self.words_freq, key = lambda x: self.words_freq[x])

        self.adjusted = None 

    def apply_adjustment(self, adjustment):
    
        self.adjusted = {'words_freq': copy.deepcopy(self.words_freq)}

        exclude = []
        if adjustment.exclude != None:
            exclude = adjustment.exclude
        
        if adjustment.freq_lim != None:
            minmax = adjustment.freq_lim           
            for word in self.words_freq:
                if (word in exclude) or not (minmax[0] <= self.words_freq[word] <= minmax[1]):
                    del(self.adjusted['words_freq'][word])
    
        if adjustment.char_lim != None:
            minmax = adjustment.char_lim
            for word in copy.deepcopy(self.adjusted['words_freq']):
                if (word in exclude) or not (minmax[0] <= len(word) <= minmax[1]):
                    del(self.adjusted['words_freq'][word])

        self.adjusted['sorted_words_by_freq'] = sorted(self.adjusted['words_freq'], key = lambda x: self.adjusted['words_freq'][x])
        
        return self.adjusted

    def hbar(self, title = '', adjustment = None, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            words_freq = self.adjusted['words_freq']
            sorted_words_by_freq = self.adjusted['sorted_words_by_freq']
        else:
            words_freq = self.words_freq
            sorted_words_by_freq = self.sorted_words_by_freq
            
        fig, ax = plt.subplots(1,1)
        
        ax.set_yticks([3*index for index in range(len(words_freq))])
        ax.set_yticklabels(sorted_words_by_freq, fontsize = 6)
        ax.set_title(title)
        
        for index in range(len(words_freq)):
            
            ax.barh(3*index, words_freq[sorted_words_by_freq[index]], \
                    color = (0, 0.25, float(index)/float(len(words_freq))))

        default_summary = "Word \'"+sorted_words_by_freq[0]+"\' appeared "+str(words_freq[sorted_words_by_freq[0]])+\
                  " times, and word \'"+sorted_words_by_freq[-1]+"\' appeared "+str(words_freq[sorted_words_by_freq[-1]])+' times.'
        plt.tight_layout()
        plt.title(title+"\n\n"+default_summary, size = 8)
        plt.show()

    def cbar(self, title = '', adjustment = None, **kwargs):

        if adjustment != None:
            self.apply_adjustment(adjustment)
            words_freq = self.adjusted['words_freq']
            sorted_words_by_freq = self.adjusted['sorted_words_by_freq']
        else:
            words_freq = self.words_freq
            sorted_words_by_freq = self.sorted_words_by_freq

        if len(sorted_words_by_freq) == 0:
            raise AssertionError()
            return None

        fig, ax = plt.subplots(1,1)

        cbar.cbar(ax, list(range(len(words_freq))), \
                  [words_freq[sorted_words_by_freq[index]] for index in range(len(words_freq))], \
                  50, [(0, 0.25, float(index)/float(len(words_freq))) for index in range(len(words_freq)) ], \
                  label = sorted_words_by_freq)

        default_summary = "Word \'"+sorted_words_by_freq[0]+"\' appeared "+str(words_freq[sorted_words_by_freq[0]])+\
                  " times, and word \'"+sorted_words_by_freq[-1]+"\' appeared "+str(words_freq[sorted_words_by_freq[-1]])+' times.'
        plt.tight_layout()
        plt.axis('off')
        plt.title(title+"\n\n"+default_summary, size = 8)
        plt.show()

        
class LinkedWords(Words):

    def __init__(self, tweet_stats_list, target_word):

        self.high_level_summary = HighLevelSummary(tweet_stats_list)
        dummy = self.high_level_summary.stats 
        self.stats = [tweet for tweet in dummy if target_word in tweet.text]
        self.target_word = target_word
        self.texts = [tweet.text for tweet in self.stats]
        self.words = func.texts_to_words(self.texts)

        self.words_unique = set(self.words)
        
        self.words_freq = {}
        for word in self.words_unique:
            self.words_freq[word] = self.words.count(word)
    
        self.sorted_words_by_freq = sorted(self.words_freq, key = lambda x: self.words_freq[x])

        self.adjusted = None
