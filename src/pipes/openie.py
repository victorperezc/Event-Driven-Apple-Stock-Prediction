from .pipe import Pipe
import contextlib
from openie import StanfordOpenIE
import pandas as pd
from nltk.corpus import wordnet as wn
class OpenIE(Pipe):
    
    __name__ = "Open Information Extraction"
    __kwargs__ = {
        '_keyword' : {'required':True},
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        structured_tweets = []

        with contextlib.redirect_stdout(None):
            with StanfordOpenIE() as client:
                for index, item in context['_data'].iterrows():
                    triples = []
                    for triple in client.annotate(item['content']):
                        if triple['subject'] != '' and triple['relation'] != '' and triple['object'] != '':
                            if self._keyword in triple['subject'] or self._keyword in triple['object']:
                                relation_pos = wn.synsets(triple['relation'])
                                if len(relation_pos):
                                    if relation_pos[0].pos() == 'v':
                                        triple['date'] = item['date']
                                        triples.append(triple)

                    if len(triples):
                        sorted(triples, key=lambda x: len(x['object']))
                        structured_tweets.append(triples[-1])

        x = {'_data': pd.DataFrame(data=structured_tweets).drop_duplicates(subset=['subject','relation','object'])}
        return x
