import numpy
from statistweepy import collection
from statistweepy import models
import matplotlib.pyplot as plt

stats = numpy.load('/home/asus/statistweepy/testfile.npy')

Authors = models.Authors(stats, filter_unique = True)

fig, ax = plt.subplots(1, 1)
Authors.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following')
plt.show()

fig, ax = plt.subplots(1, 1)
Authors.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Following')
plt.show()
