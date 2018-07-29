import tweepy

def filter_unique(tweet_stats_list, output = 'status'):
    
    uniques = set()
    
    for tweet in tweet_stats_list:

        if not isinstance(tweet, tweepy.Status):
            raise TypeError('Each element must be of tweepy.Status object')
            
        try:
            tweet = tweet.retweeted_status
        except:
            pass

        if tweet.id not in uniques:

            uniques.add(tweet.id)

            if output == 'text':

                try:
                    yield tweet.text
                except:
                    yield tweet.full_text

            yield tweet

def split_texts(texts):

        for text in texts:

            yield text.split()

def total_rts(tweet_stats_list, string_inclusion = False):

    result = 0

    if not string_inclusion :

        result = sum([tweet.retweet_count for tweet in tweet_stats_list]);

    else:

        try:
            result = sum([tweet.retweet_count for tweet in tweet_stats_list if string_inclusion in tweet.full_text.split()])
        except:
            result = sum([tweet.retweet_count for tweet in tweet_stats_list if string_inclusion in tweet.text.split()])

    return result
