from  .pipe import Pipe
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

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


class TfIdf(Pipe):

    __name__ = "TF IDF"
    __kwargs__ = {
        '_csv': {'required':False,'default':None}
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def tfidf(self,dataset):
        tfidf = TfidfVectorizer(use_idf=True)
        tfidf.fit(dataset)
        return tfidf

    def score(self,tfidf,text):
        feature_names = tfidf.get_feature_names()
        tfidf_matrix= tfidf.transform([text]).todense()
        feature_index = tfidf_matrix[0,:].nonzero()[1]
        tfidf_scores = zip([feature_names[i] for i in feature_index], [tfidf_matrix[0, x] for x in feature_index])
        return sum(dict(tfidf_scores).values())

    def process(self, context):
        super().process()

        subject_tfidf = self.tfidf(context['_data']['subject'])
        relation_tfidf = self.tfidf(context['_data']['relation'])
        object_tfidf = self.tfidf(context['_data']['object'])

        encoded_tweets = []
        for _,tweet in context['_data'].iterrows():
            encoded_tweet = {}
            encoded_tweet['subject'] = self.score(subject_tfidf,tweet['subject'])
            encoded_tweet['relation'] = self.score(relation_tfidf,tweet['relation'])
            encoded_tweet['object'] = self.score(object_tfidf,tweet['object'])
            encoded_tweet['timestamp'] = tweet['date'].strftime("%Y-%m-%d")
            encoded_tweets.append(encoded_tweet)
        
        encoded_tweets = pd.DataFrame(data=encoded_tweets)

        if self._csv:
            encoded_tweets.to_csv(self._csv,index=False)

        return {'_data':encoded_tweets}

