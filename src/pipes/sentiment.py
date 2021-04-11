from .pipe import Pipe
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment(Pipe):
    
    __name__ = "Sentiment Compute"

    def __init__(self,**kwargs):
        self.analyzer = SentimentIntensityAnalyzer()
        super().__init__(**kwargs)

    def process(self,context):
        super().process()

        vs = self.analyzer.polarity_scores(context['_data'])
        
        if vs["compound"] < -0.05:
            return "negative",vs["compound"]
        elif vs["compound"] > 0.05:
            return "positive",vs["compound"]
        else:
            return "neutral",vs["compound"]

        return {
            '_data':  [ re.sub(r'http\S+', '', item) for item in context['_data'] ] 
        }
    
    @property
    def allowed_keys(self):
        return {'_data'}
