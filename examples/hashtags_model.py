import numpy
from statistweepy.models import Tweets
from statistweepy.models import Hashtags
from statistweepy.adjustment import Adjustment
import matplotlib.pyplot as plt

stats = numpy.load('/home/asus/statistweepy/testfile.npy')
tweets = Tweets(stats)

Model = Hashtags(tweets)

Adjust = Adjustment(freq_lim = (2, 199), char_lim = (3, 11111));

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, adjustment = Adjust, height = 0.5, color = 'orange')

fig, ax = plt.subplots(1, 1)
Model.rbar_plot(ax, adjustment = Adjust, color  = 'orange', bar_width = 6, textsize = 10, base_radius = 70)

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, adjustment = Adjust, height = 0.5, color = 'pink', incolor_rt = True)

fig, ax = plt.subplots(1, 1)
Model.rbar_plot(ax, adjustment = Adjust, color  = 'pink', incolor_rt = True, bar_width = 6, textsize = 10, base_radius = 70)

plt.show()
