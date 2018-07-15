import numpy
from statistweepy import models
import matplotlib.pyplot as plt
import statistweepy.adjustment as adjust
import statistweepy.functionals as func

stats = numpy.load('testfile.npy')

Splits = models.Splits(stats, filter_unique = True)

Adjust = adjust.Adjustment(freq_lim = (5, 199), exclude = ('di', 'ke', 'dari'), char_lim = (3, 11111));

fig, ax = plt.subplots(1, 1)
Splits.hbar_plot(ax, title = '', adjustment = Adjust, color = 'orange')
plt.show()

fig, ax = plt.subplots(1, 1)
Splits.rbar_plot(ax, title = '', adjustment = Adjust, color  = 'magenta', bar_width = 6, textsize = 10, base_radius = 70)
plt.show()

fig, ax = plt.subplots(1, 1)
Splits.hbar_plot(ax, title = '', adjustment = Adjust, color = (0,0,1,1), incolor_rt = True)

fig, ax = plt.subplots(1, 1)
Splits.rbar_plot(ax, title = '', adjustment = Adjust, color  = (0,0,1,1), incolor_rt = True, bar_width = 6, textsize = 10, base_radius = 70)
plt.show()
