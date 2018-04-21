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

def texts_to_words(texts, adjustment = None):

        word_list = []
        for text in texts:
            words = text.split()
            if adjustment != None:
                for group in adjustment.group:
                    words = adjust.group(words, group, group.name)
            word_list.extend(words)

        return word_list
