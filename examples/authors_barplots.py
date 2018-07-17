import numpy
from statistweepy.models import Authors
from statistweepy.models import Tweets
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')
tweets = Tweets(stats)

Model = Authors(stats)

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following', height = 0.5, color = (1,0,0,1))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Followers', height = 0.5, color = (1,0,0,1))
plt.show()
