import numpy
from statistweepy import models
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')

Authors = models.Authors(stats, filter_unique = True)

fig, ax = plt.subplots(1, 1)
Authors.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following', textsize = 8, width = 0.5, color = (1,0,0,1))

fig, ax = plt.subplots(1, 1)
Authors.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Followers', textsize = 8, width = 0.5, color = (1,0,0,1))
plt.show()
