#Author : anbarief@live.com

import copy


def group(strings, group_list = [], name = ''):
    new = copy.deepcopy(strings)
    for i in range(len(new)):        
        if new[i] in group_list:
            new[i] = name
    return new 


class Group(list):

    def __init__(self, strings, name):
        list.__init__(self, strings)
        self.name = name

    
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

        if 'group' in kwargs:
            self.group = kwargs['group']
        else:
            self.group = None

        if 'exclude' in kwargs:
            self.exclude = kwargs['exclude']
        else:
            self.exclude = None
