import tweepy
import string

def filter_unique(tweets):

    uniques = set()
    
    for tweet in tweets:

        if not isinstance(tweet, tweepy.Status):
            raise TypeError('Each element must be of tweepy.Status object')
            
        try:
            tweet = tweet.retweeted_status
        except:
            pass

        if tweet.id not in uniques:

            uniques.add(tweet.id)

            yield tweet

def clean_text(text):

    punct = string.punctuation
    printable = string.printable
    whitespace = string.whitespace

    table = text.maketrans({key: None for key in printable})
    undef = set(text.translate(table))

    table = text.maketrans({key: None for key in undef})
    removed_undef = text.translate(table)

    table = text.maketrans({key: None for key in punct})
    cleaned = removed_undef.translate(table)

    table = text.maketrans({key: ' ' for key in whitespace})
    cleaned = cleaned.translate(table)

    return cleaned

def split_texts(texts, naive):

    if naive:
        for text in texts:
            yield text.split()
    else:
        for text in texts:
            yield clean_text(text).split()

def total_rts(tweets, string_inclusion = False, naive = True):

    result = 0

    if not string_inclusion :

        result = sum([tweet.retweet_count for tweet in tweets]);

    else:

        if naive:
            try:
                result = sum([tweet.retweet_count for tweet in tweets if string_inclusion in tweet.full_text.split()])
            except:
                result = sum([tweet.retweet_count for tweet in tweets if string_inclusion in tweet.text.split()])
        else:
            try:
                result = sum([tweet.retweet_count for tweet in tweets if string_inclusion in clean_text(tweet.full_text).split()])
            except:
                result = sum([tweet.retweet_count for tweet in tweets if string_inclusion in clean_text(tweet.text).split()])
            
    return result
