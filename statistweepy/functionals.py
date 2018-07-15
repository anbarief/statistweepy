def filter_unique(tweet_stats_list, output = 'status'):

    stats = tweet_stats_list
    unique = []

    for tweet in stats:
            
        try:
            if not tweet.retweeted_status in unique:
                if output == 'status':
                    unique.append(tweet.retweeted_status)
                elif output == 'text':
                    unique.append(tweet.retweeted_status.text)
                        
        except:
            if not tweet in unique:
                if output == 'status':
                    unique.append(tweet)
                elif output == 'text':
                    unique.append(tweet.text)

    return unique

def split_texts(texts, adjustment = None):
        split_list = []
        for text in texts:
            split = text.split()
            split_list.extend(split)
        return split_list

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
