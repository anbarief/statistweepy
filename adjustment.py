#Author : anbarief@live.com

import copy

    
class Adjustment(object):

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
