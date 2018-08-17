# author : Arief Anbiya (anbarief@live.com)
# Algorithm for the visualization

import numpy
sqrt = numpy.sqrt
cos = numpy.cos
sin = numpy.sin
pi =  numpy.pi
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import colors as mplcolors
from statistweepy import utils
from statistweepy import models
import operator
import itertools

def rbar(ax, radii, radius, col, label, bar_width = 5, text_size = 7):

   n = len(radii)
   indexs = range(n)

   x = [-radius+i*0.01 for i in range(2*100*radius + 1)]
   y_upper = [sqrt(radius**2 - i**2) for i in x]
   y_lower = [-y for y in y_upper]

   ax.plot(x, y_upper, color = 'k')
   ax.plot(x, y_lower, color = 'k')
   
   dr = float(1)/float(n)

   indicator = 1
   
   for index in indexs:

      rx = (radius+((1/50)*radius)*radii[index])*cos(dr*index*2*pi)
      ry = (radius+((1/50)*radius)*radii[index])*sin(dr*index*2*pi)

      cx = radius*cos(dr*index*2*pi)
      cy = radius*sin(dr*index*2*pi)
       
      ax.plot([cx, rx], \
              [cy, ry], \
              lw = bar_width, color = col[index])

      degree = (dr*index*2*pi)*360/(2*pi)

      ha_split = 'right'
      ha_text = 'left'
      degree_split = degree
      degree_freq = degree
      
      if 90 < degree < 270 :

         degree_split = -(180-degree)
         ha_split = 'left'
         
      split = label[index]

      Rx = (radius+((1/50)*radius)*max(radii))*cos(dr*index*2*pi)
      Ry = (radius+((1/50)*radius)*max(radii))*sin(dr*index*2*pi)
      
      text = ax.text(1.5*Rx, 1.5*Ry, split+' ('+str(radii[index])+')', ha = ha_split, va = 'center', rotation = degree_split, rotation_mode = 'anchor', size = text_size)
      
      ax.plot([rx, 1.5*Rx], \
              [ry, 1.5*Ry], \
              lw = 0.5, color = 'gray')
      
   ax.set_aspect('equal')

def hbar_plot_Authors(model, ax, meas = 'followers_count', color = (0,0,1,1), incolor_meas = None, space = True, text_sizes = [7, 12], freq_lim = None):

    if not isinstance(model, models.Authors):
       raise TypeError("model must be a statistweepy.models.Authors object.")

    width = 5

    if freq_lim != None:
       dic = getattr(model, meas)
       meas_dic = {key: dic[key] for key in dic.keys() if freq_lim[0] <= dic[key] <= freq_lim[1]}
    else:
       meas_dic = getattr(model, meas)
       
    sorted_authors = sorted(meas_dic, key = lambda x : meas_dic[x])

    if isinstance(color, str):
            
        color = mplcolors.hex2color(mplcolors.cnames[color])        
        
    colors = len(meas_dic)*[color]
    if incolor_meas != None:

        icdic = getattr(model, incolor_meas)
        meas_icdic = {key: icdic[key] for key in meas_dic.keys()}
        minor_max = max(meas_icdic.values())
        transparency = [meas_icdic[author]/minor_max for author in sorted_authors]
        colors = [(color[0], color[1], color[2], trans) for trans in transparency]

    if space:
        space = width
    else:
        space = 0

    var = ( 1 +  i*(space + width)  for i in range(len(meas_dic)) )

    bar_pos = []; ytick_pos = []

    for i in var:

        bar_pos.append(i - width/2) 
        ytick_pos.append(i)
        
    ax.barh(bar_pos, [meas_dic[author] for author in sorted_authors], height = width, color = colors)
    ax.set_yticks(ytick_pos)
    helvetica = fm.FontProperties(fname = '/home/asus/statistweepy/fonts/HelveticaNeueBold.ttf', size = text_sizes[0])
    ax.set_yticklabels(sorted_authors, rotation = 'horizontal', fontproperties = helvetica)

    ax.set_ylim([1 - width/2 - space, max(ytick_pos) + width/2 + space])

    if incolor_meas != None:
            
        ax.set_xlabel(meas + ' (color : '+incolor_meas+')', size = text_sizes[1])

    else :

        ax.set_xlabel(meas, size = text_sizes[1])

    plt.tight_layout()

def hbar2sided_plot_Authors(model, ax, meas_left = 'followers_count', meas_right = 'following_count', colors = ['red', 'blue'], incolor_meas = None, space = True, text_sizes = [7, 10], aux_size = 5, freq_lim = (None, None)):

    if not isinstance(model, models.Authors):
       raise TypeError("model must be a statistweepy.models.Authors object.")

    width = 5

    if freq_lim[0] != None:
       leftdic = getattr(model, meas_left)
       rightdic = getattr(model, meas_right)
       if freq_lim[0] == 'left':
          meas_leftdic = {key: leftdic[key] for key in leftdic.keys() if freq_lim[1][0] <= leftdic[key] <= freq_lim[1][1]}
          meas_rightdic = {key: rightdic[key] for key in meas_leftdic.keys()}
       elif freq_lim[0] == 'right':
          meas_rightdic = {key: rightdic[key] for key in rightdic.keys() if freq_lim[1][0] <= rightdic[key] <= freq_lim[1][1]}
          meas_leftdic = {key: leftdic[key] for key in meas_rightdic.keys()}
    else:
       meas_leftdic = getattr(model, meas_left)
       meas_rightdic = getattr(model, meas_right)

    if isinstance(colors[0], str):
        color_left = mplcolors.hex2color(mplcolors.cnames[colors[0]])

    if isinstance(colors[1], str):            
        color_right = mplcolors.hex2color(mplcolors.cnames[colors[1]])
      
    colors_left = len(meas_leftdic)*[color_left]
    colors_right = len(colors_left)*[color_right]

    if incolor_meas != None:
        dic = getattr(model, incolor_meas)
        if freq_lim[0] != None:
           incolor = {key : dic[key] for key in meas_leftdic}
        else:
           incolor = dic
        minor_max = max(incolor.values())
        trans_both = [incolor[author]/minor_max for author in meas_leftdic.keys()]
        colors_left = [(color_left[0], color_left[1], color_left[2], trans) for trans in trans_both]
        colors_right = [(color_right[0], color_right[1], color_right[2], trans) for trans in trans_both]
        
    if space:
        space = width
    else:
        space = 0

    var = ( 1 +  i*(space + width)  for i in range(len(colors_left)) )

    bar_pos = []; ytick_pos = []

    for i in var:

        bar_pos.append(i - width/2) 
        ytick_pos.append(i)

    left_values = [-meas_leftdic[author] for author in meas_leftdic.keys()]
    right_values = [meas_rightdic[author] for author in meas_leftdic.keys()]
    ax.barh(bar_pos, left_values, left = -1, height = width, color = colors_left)
    ax.barh(bar_pos, right_values, left = 1, height = width, color = colors_right)

    xlim = ax.get_xlim()
    ax.set_yticks(ytick_pos)
    for i in ytick_pos:
       ax.plot([xlim[0], 0], [i, i], '--', color = 'gray', linewidth = aux_size)

    helvetica = fm.FontProperties(fname = '/home/asus/statistweepy/fonts/HelveticaNeueBold.ttf', size = text_sizes[0])
    ax.set_yticklabels(meas_leftdic.keys(), rotation = 'horizontal', fontproperties = helvetica)

    ax.set_xticks([min(left_values), max(right_values)])
    ax.set_xticklabels([str(-min(left_values)), str(max(right_values))])

    ax.set_ylim([1 - width/2 - space, max(ytick_pos) + width/2 + space])

    if incolor_meas != None:
            
        ax.set_xlabel('left side : {}, right side : {}, (color : {})'.format(meas_left, meas_right, incolor_meas), size = text_sizes[1])

    else :

        ax.set_xlabel('left side : {}, right side : {}'.format(meas_left, meas_right), size = text_sizes[1])

    plt.tight_layout()

def scatter_plot_Authors(model, ax, meas_x='followers_count', meas_y='following_count', incolor_meas = None, marker_size = 10, color = 'blue', text_sizes = [20, 10]):

   if not isinstance(model, models.Authors):
      raise TypeError("model must be a statistweepy.models.Authors")

   if isinstance(color, str):
        color = mplcolors.hex2color(mplcolors.cnames[color])        

   meas_xdic = getattr(model, meas_x)
   meas_ydic = getattr(model, meas_y)
      
   authors = model.authors_tweets.keys()
   helvetica = fm.FontProperties(fname = '/home/asus/statistweepy/fonts/HelveticaNeueBold.ttf', size = text_sizes[0])

   if incolor_meas != None:
      meas_icdic = getattr(model, incolor_meas)
      icmax = max(meas_icdic.values())

   for author in authors:
      x=meas_xdic[author]
      y=meas_ydic[author]
      if incolor_meas != None:
         trans = meas_icdic[author]/icmax
      else:
         trans = 0.6
      ax.plot(x, y, 'o', markersize = marker_size, color = [color[0], color[1], color[2], trans], markeredgecolor = 'black', markeredgewidth = 1)
      ax.text(x, y, author, fontproperties = helvetica)
   ax.margins(0.2)
   
   ax.set_xlabel(meas_x, size = text_sizes[1])
   ax.set_ylabel(meas_y, size = text_sizes[1])
   
   plt.tight_layout()

def hbar_plot_Splits(model, ax, adjustment = None, color = (0, 0.6, 1, 1), incolor = None, space = True, text_sizes = [7, 12]):

    if not isinstance(model, models.Splits):
       raise TypeError("model must be a statistweepy.models.Splits object.")

    width = 5
        
    if adjustment != None:
            
        model.apply_adjustment(adjustment)
        splits_freq = model.adjusted['splits_freq']
        sorted_splits_by_freq = model.adjusted['sorted_splits_by_freq']

    else:

        splits_freq = model.splits_freq
        sorted_splits_by_freq = model.sorted_splits_by_freq

    if isinstance(color, str):

        color = mplcolors.hex2color(mplcolors.cnames[color])        

    if incolor == 'retweets':

        sorted_total_rts = [utils.total_rts(model.tweets, string_inclusion = split, naive = model.naive) for split in sorted_splits_by_freq]
        max_total_rts = max(sorted_total_rts)
        col = [(color[0], color[1], color[2], total_rts/max_total_rts) for total_rts in sorted_total_rts]

    elif incolor == 'likes':

        sorted_total_likes = [utils.total_likes(model.tweets, string_inclusion = split, naive = model.naive) for split in sorted_splits_by_freq]
        max_total_likes = max(sorted_total_likes)
        col = [(color[0], color[1], color[2], total_likes/max_total_likes) for total_likes in sorted_total_likes]
       
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
    helvetica = fm.FontProperties(fname = '/home/asus/statistweepy/fonts/HelveticaNeueBold.ttf', size = text_sizes[0])
    ax.set_yticklabels(sorted_splits_by_freq, rotation = 'horizontal', fontproperties = helvetica)
    ax.set_ylim([1 - width/2 - space, max(ytick_pos) + width/2 + space])

    if incolor == 'retweets':
            
        ax.set_xlabel('Splits frequency count. (color : total retweets)', size = text_sizes[1])

    elif incolor == 'likes':

        ax.set_xlabel('Splits frequency count. (color : total likes)', size = text_sizes[1])

    else :

        ax.set_xlabel('Splits frequency count.')
            
    plt.tight_layout()

def rbar_plot_Splits(model, ax, adjustment = None, base_radius = 50, bar_width = 6, color = (0, 0, 1, 1), text_sizes = [7, 12]):

    if not isinstance(model, models.Splits):
       raise TypeError("model must be a statistweepy.models.Splits")
        
    if adjustment != None:
            
        model.apply_adjustment(adjustment)
        splits_freq = model.adjusted['splits_freq']
        sorted_splits_by_freq = model.adjusted['sorted_splits_by_freq']

    else:

        splits_freq = model.splits_freq
        sorted_splits_by_freq = model.sorted_splits_by_freq

    if isinstance(color, str):

        color = mplcolors.hex2color(mplcolors.cnames[color])        

    colors = [color]*len(splits_freq)
         
    rbar(ax, [splits_freq[sorted_splits_by_freq[index]] for index in range(len(splits_freq))], \
                  base_radius, col = colors, \
                  label = sorted_splits_by_freq, bar_width = bar_width, text_size = text_sizes[0])
            
    ax.tick_params(colors=(0,0,0,0))

    ax.set_xlabel('Splits frequency count.', size = text_sizes[1])
        
    plt.tight_layout()

def time_distribution(model, ax, unit = 'hour', **kwargs):

   if not isinstance(model, models.Tweets):
      raise TypeError(' model must be of statistweepy.models.Tweets ')

   if not any([unit == 'year', unit == 'month', unit == 'day', unit == 'hour']):
      raise AssertionError(' The argument unit must be one of \'year\',  \'month\',  \'day\', or \'hour\'. ')
            
   unicity_key = operator.attrgetter('created_at.'+unit)
   tweets = sorted(model, key=unicity_key)
   distribution = {}

   for time, time_tweets in itertools.groupby(tweets, key=unicity_key):

      time_tweets = list(time_tweets)      
      distribution[time] = len(time_tweets)
      fy = lambda x: x

   if unit == 'year':
                
      xt = [tweet.created_at.year + (tweet.created_at.month + (tweet.created_at.day + tweet.created_at.hour/24)/31)/12 \
            for tweet in model]

      a = int(min(xt))
      b = int(max(xt))
      ticks = range(a-1, b+2)

   elif unit == 'month':
                
      xt = [(tweet.created_at.month + (tweet.created_at.day + tweet.created_at.hour/24)/31) \
            for tweet in model]

      ticks = range(1, 13)

   elif unit == 'day':
                
      xt = [(tweet.created_at.day + tweet.created_at.hour/24) \
            for tweet in model]

      ticks = range(1, 32)

   elif unit == 'hour':

      xt = [tweet.created_at.hour + (tweet.created_at.minute + tweet.created_at.second/60)/60 \
            for tweet in model]
                
      ticks = range(0, 25)

   histogram = ax.hist(xt, **kwargs)
   ax.set_xticks(ticks)
   ax.set_xticklabels([str(i) for i in ticks])
   ax.set_xlabel(unit)
   ax.set_ylabel('frequency')
            
   return distribution, histogram
