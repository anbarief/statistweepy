# statistweepy (v.0.1)
A (still in work) simple tool that use tweepy to collect and use Twitter data. The data structure is simple `Status` object collected using tweepy. To collect the data you must have a 'consumer key', 'consumer secret', 'access token', and 'access secret', that can be obtained by [register for a Twitter application](http://apps.twitter.com/). These will be used to access Twitter API through your Twitter account, and should be kept private. Notice also that you should *read and peruse the Twitter Developer Agreement and Policy carefully*, you may not use the data carelessly for example to do surveillance, provoke negative conflicts, etc.

Requirements :
- [Tweepy](http://docs.tweepy.org/en/v3.5.0/)
- Numpy
- Matplotlib

Author : Arief Anbiya (anbarief@live.com), written in Python 3.

Useful article(s) : 

https://www.linkedin.com/pulse/model-data-analyzing-twitter-using-python-tweepy-arief-anbiya/?published=t

https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

---------------------------------

## Work Cycle : (Pose the Question) - Collect Data - Analyze Data - (Interpret Results)

## Collect Data :

Here is an example of how we can collect the data : 

```
from statistweepy.collection import Authentication
from statistweepy.collection import Collection

consumer_key = '****'
consumer_secret = '****'
access_token = '****'
access_secret = '****'

Auth = Authentication(consumer_key, consumer_secret, access_token, access_secret)
Collect = Collection(Auth)

data = Collect.collect_home()
```
This first creates an 'authentication' object of `Authentication`, which access the Twitter API. This object is then required as input for `Collection` class. To use the Twitter data, get the first index of `data`, `stats = data[0]`. The 2nd index is the collection time.

```
>>> print(data[1])
hour_min_16_53_date_29_7_2018
```

----------------------------

## Analyze Data :

Currently, there are three models, setup in `Tweets`, `Authors`, and `Splits` class. 

---------------------------

We will see how we can use `Tweets` class:

```
import numpy
from statistweepy.models import Tweets

stats = numpy.load('testfile.npy')
tweets = Tweets(stats)
```
This will create a `Tweets` object named `tweets`, which is a list-like object containing tweets (`tweepy.models.Status` objects).

```
>>> tweets
[0]: \U0001f60d

#FRACRO // #WorldCupFinal https://t.co/w227YQWA0A
.
.
.
[191]: VIDEO: Antusias Warga Kroasia Jelang Final Piala Dunia 2018 https://t.co/68bQixTqNF
```
As you can see above, `len(tweets)` will give `192`.

Filtering by an author's name:

```
>>> tweets.filter_by_name('Reuters Top News')
[0]: Iran's supreme leader calls for government to be backed in face of U.S. sanctions https://t.co/E8EDZBO0MP
.
.
.
[30]: Iraq police fire in air as protesters try to storm Basra government building https://t.co/LsfQe5Hrrb https://t.co/wTbCUFhTdy
```

Filtering by an author's username:

```
>>> tweets.filter_by_name('Reuters')
[0]: Iran's supreme leader calls for government to be backed in face of U.S. sanctions https://t.co/E8EDZBO0MP
.
.
.
[30]: Iraq police fire in air as protesters try to storm Basra government building https://t.co/LsfQe5Hrrb https://t.co/wTbCUFhTdy
```
Filtering by time interval: (in this example we will get only tweets appeared between 1 Jan 2017 and 1 Jan 2018)

```
>>> import datetime
>>> a = datetime.datetime(2017, 1, 1); b = datetime.datetime(2018, 1, 1)
>>> tweets.filter_by_time_interval([a,b])
[0]: Masyarakat Temanggung dukung Asian Games 2018. Hokyaaa !!! \U0001f604
~ @ganjarpranowo ~

#Temanggung  
#AsianGames2018\u2026 https://t.co/gq6IwXyYWZ
.
.
.
[1]: Cecil Wayne Ratliff - Wrote the database program Vulcan. https://t.co/14B54dcKW6
>>> tweets_filtered = _
```
As you can see, only two tweets that match.

------------------------

We will see one example of using `Authors` model:

```
import numpy
from statistweepy.models import Authors
from statistweepy.models import Tweets
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')

Model = Authors(Tweets(stats))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following', text_size = 8, width = 0.5, color = (0, 0.6, 1, 1))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Followers', text_size = 8, width = 0.5, color = (0, 0.6, 1, 1))

plt.show()
```
![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_1.png)

The 1st plot shows the number of followers of each appearing account in the data, with the color representing the number of followed accounts. The denser color has more accounts followed.

![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_2.png)

The 2nd plot shows the number of sample tweets in the data of each appearing account, with the color representing the number of followers. The denser color has more followers.

------------------------

We will see one example of using `Authors` model:

```
import numpy
from statistweepy.models import Authors
from statistweepy.models import Tweets
import matplotlib.pyplot as plt

stats = numpy.load('testfile.npy')

Model = Authors(Tweets(stats))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Followers', incolor_measurement = 'Following', text_size = 8, width = 0.5, color = (0, 0.6, 1, 1))

fig, ax = plt.subplots(1, 1)
Model.hbar_plot(ax, measurement = 'Sample Tweets', incolor_measurement = 'Followers', text_size = 8, width = 0.5, color = (0, 0.6, 1, 1))

plt.show()
```
![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_1.png)

The 1st plot shows the number of followers of each appearing account in the data, with the color representing the number of followed accounts. The denser color has more accounts followed.

![alt text](https://raw.githubusercontent.com/anbarief/statistweepy/master/readme_2.png)

The 2nd plot shows the number of sample tweets in the data of each appearing account, with the color representing the number of followers. The denser color has more followers.







