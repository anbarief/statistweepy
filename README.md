# statistweepy
A (still in work) simple tool that use tweepy to collect and use Twitter data. The data structure is simple `Status` object collected using tweepy. To collect the data you must have a 'consumer key', 'consumer secret', 'access token', and 'access secret', that can be obtained by [register for a Twitter application](http://apps.twitter.com/). These will be used to access Twitter API through your Twitter account, and should be kept private. Notice also that you should *read and peruse the Twitter Developer Agreement and Policy carefully*, you may not use the data carelessly for example to do surveillance, provoke negative conflicts, etc.

Requirements :
- [Tweepy](http://docs.tweepy.org/en/v3.5.0/)
- Numpy
- Matplotlib

Author : Arief Anbiya (anbarief@live.com), written in Python 3.

## Work Cycle : (Pose the Question) - Collect Data - Analyze Data - (Interpret Results)

## Collect Data :

Here is an example of how we can collect the data : 

```
import statistweepy.collection as collection
consumer_key = '****'
consumer_secret = '****'
access_token = '****'
access_secret = '****'
init = collection.Authentication(consumer_key, consumer_secret, access_token, access_secret) 
collect = collection.Collection(Init)
```
This first creates an 'authentication' object of `Authentication`, which access the Twitter API. This object is then required as input for `Collection` class. 

## Analyze Data :

Currently, there are only two models, setup in `Authors` class and `Splits` class. We will see one example of using `Authors` model.

```
import numpy
from statistweepy.models import Authors
from statistweepy.models import Tweets
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')

Model = Authors(Tweets(stats))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following', textsize = 8, height = 0.5, color = (0, 0.6, 1, 1))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Followers', textsize = 8, height = 0.5, color = (0, 0.6, 1, 1))

plt.show()
```
![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_1.png)

The 1st plot shows the number of followers of each appearing account in the data, with the color representing the number of followed accounts. The denser color has more accounts followed.

![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_2.png)

The 2nd plot shows the number of sample tweets in the data of each appearing account, with the color representing the number of followers. The denser color has more followers.




