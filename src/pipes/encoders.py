from  .pipe import Pipe
import pandas as pd
class BasicTextEncoder(Pipe):

    __name__ = "Basic Text Encoder"
    __kwargs__ = {}

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self, context):
        super().process()

        vocabulary = []
        for _,item in context['_data'].iterrows():
            for word in ' '.join([item['subject'],item['relation'],item['object']]).split():
                if word not in vocabulary:
                    vocabulary.append(word)

        ## encode vocabulary by index

        encoded_tweets = []
        for _,tweet in context['_data'].iterrows():
            encoded_tweet = {}
            encoded_tweet['subject'] = sum([vocabulary.index(word) for word in tweet['subject'].split()])/len(tweet['subject'].split())
            encoded_tweet['relation'] = sum([vocabulary.index(word) for word in tweet['relation'].split()])/len(tweet['relation'].split())
            encoded_tweet['object'] = sum([vocabulary.index(word) for word in tweet['object'].split()])/len(tweet['object'].split())
            encoded_tweet['timestamp'] = tweet['date'].strftime("%Y-%m-%d")
            encoded_tweets.append(encoded_tweet)

        encoded_tweets = pd.DataFrame(data=encoded_tweets)
        return {'_data':encoded_tweets}



