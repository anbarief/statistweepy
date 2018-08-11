# author : Arief Anbiya (anbarief@live.com)
# Algorithm for the visualization

import numpy
sqrt = numpy.sqrt
cos = numpy.cos
sin = numpy.sin
pi =  numpy.pi
import matplotlib.pyplot as plt
from matplotlib import colors as mplcolors
from statistweepy import utils
from statistweepy import models
import operator
import itertools

def rbar_A(ax, radii, radius, col, label, bar_width = 5, text_size = 7):

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

def rbar_B(ax, radii, radius, col, label, bar_width = 5, text_size = 7):

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

      ax.plot([radius*cos(dr*indexs[index]*2*pi), rx], \
            [radius*sin(dr*indexs[index]*2*pi), ry], \
               lw = bar_width, color = col[index])

      deg = (float(1)/float(2*pi))*(dr*indexs[index]*2*pi)*360
      lab = label[index]

      if dr*indexs[index]*2*pi >= 0.5*pi and  dr*indexs[index]*2*pi <= 1.5*pi:

         deg = deg + (float(1)/float(2*pi))*pi*360

      if index%2 == 0:

         tx = (radius+radii[index] + (2/10)*radius)*cos(dr*indexs[index]*2*pi)
         ty = (radius+radii[index] + (2/10)*radius)*sin(dr*indexs[index]*2*pi)
  
      else:

         indicator *= -1
         if indicator == 1:

            tx = (radius + (1/20)*radius)*cos(dr*indexs[index]*2*pi)
            ty = (radius + (1/20)*radius)*sin(dr*indexs[index]*2*pi)

         else:

            tx = (radius - (1/10)*radius)*cos(dr*indexs[index]*2*pi)
            ty = (radius - (1/10)*radius)*sin(dr*indexs[index]*2*pi)
   
      ax.text(tx, \
               ty, \
               lab + ' ('+str(radii[index])+')', ha = 'center'\
               #rotation = deg)
                , size = text_size, fontweight = 'bold'
               )

      ax.plot([tx, rx], [ty, ry], lw = 1)
           
   ax.set_aspect('equal')

def hbar_plot_Authors(model, ax, measurement = 'Followers', color = (0,0,1,1), incolor_measurement = None, space = True, text_size = 7):

    if not isinstance(model, models.Authors):
       raise TypeError("model must be a statistweepy.models.Authors object.")

    width = 5

    measurements = {'Followers': model.followers_count, \
                    'Following' : model.following_count, \
                    'Total Tweets' : model.total_tweets, \
                    'Sample Tweets' : model.sample_count}

    sorted_authors = sorted(measurements[measurement], key = lambda x : measurements[measurement][x])

    if isinstance(color, str):
            
        color = mplcolors.hex2color(mplcolors.cnames[color])        
        
    colors = len(model.authors_tweets)*[color]
    if incolor_measurement != None:
            
        minor_max = max(measurements[incolor_measurement].values())
        transparency = [measurements[incolor_measurement][author]/minor_max for author in sorted_authors]
        colors = [(color[0], color[1], color[2], trans) for trans in transparency]

    if space:
        space = width
    else:
        space = 0

    var = ( 1 +  i*(space + width)  for i in range(len(model.authors_tweets)) )

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

def hbar_plot_Splits(model, ax, adjustment = None, color = (0, 0.6, 1, 1), incolor_rt = False, space = True, text_size = 7):

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

    if incolor_rt:

        sorted_total_rts = [utils.total_rts(model.tweets, string_inclusion = split, naive = model.naive) for split in sorted_splits_by_freq]
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

def rbar_plot_Splits(model, ax, mode = 'A', adjustment = None, base_radius = 50, bar_width = 6, color = (0, 0, 1, 1), text_size = 7):

    if not isinstance(model, models.Splits):
       raise TypeError("model must be a statistweepy.models.Splits object.")
        
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

def time_distribution(model, ax, unit = 'hour', **kwargs):

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

   return distribution

def scatter_plot(model, ax):
   pass
