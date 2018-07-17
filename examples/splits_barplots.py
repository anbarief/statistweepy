import numpy
from statistweepy.models import Splits
from statistweepy.models import Tweets
from statistweepy.adjustment import Adjustment
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')
tweets = Tweets(stats)

Model = Splits(stats)

Adjust = Adjustment(freq_lim = (5, 199), exclude = ('the', 'for'), char_lim = (3, 11111));

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, adjustment = Adjust, height = 1, color = 'orange')

fig, ax = plt.subplots(1, 1)
Model.rbar_plot(ax, adjustment = Adjust, color  = 'orange', bar_width = 6, textsize = 10, base_radius = 70)

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, adjustment = Adjust, height = 0.5, color = 'pink', incolor_rt = True)

fig, ax = plt.subplots(1, 1)
Model.rbar_plot(ax, adjustment = Adjust, color  = 'pink', incolor_rt = True, bar_width = 6, textsize = 10, base_radius = 70)

plt.show()
