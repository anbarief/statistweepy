from statistweepy import models
import matplotlib.pyplot as plt
import numpy

#Use existing data
loaded = numpy.load('/home/asus/Arief_tempo/twitterstats/ProSyn_3000_12_8_2018_extended.npy')

#Use the Tweets model and viewing the first 11 tweets
tweets = models.Tweets(loaded)
tweets.view(0, 10)

#Use the Splits model
model = models.Splits(tweets, naive = False)

#Excluded words
exc_splits = ('the', 'if', 'The', 'is', 'on', 'are', 'we', 'on', 'at', 'not', 'of', 'to', \
              'than', 'and', 'for', 'that', 'be', 'it', 'in', 'or', 'as')
#Create an adjustment : only include words that appeared between 50 to 10000 times,
# and each the length of each word must be between 3 to 100.
adjustment = models.Adjustment(freq_lim = (50, 10000), char_lim = (3, 100), exclude = exc_splits)

fig, ax = plt.subplots(1, 1)
model.hbar_plot(ax, adjustment = adjustment, color = 'blue', incolor  = 'likes', text_sizes = [12, 15])

fig, ax = plt.subplots(1, 1)
model.hbar_plot(ax, adjustment = adjustment, color = 'blue', incolor  = 'retweets', text_sizes = [12, 15])

fig, ax = plt.subplots(1, 1)
model.rbar_plot(ax, adjustment = adjustment, color = (1, 0, 0, 1), bar_width = 3, base_radius = 100, text_sizes = [12, 15])

plt.show(block = False)
