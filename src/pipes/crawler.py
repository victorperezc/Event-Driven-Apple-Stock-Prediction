from .pipe import Pipe
import snscrape.modules.twitter as sntwitter
import itertools
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class TwitterCrawler(Pipe):

    __name__ = "Twitter Crawler"
    __kwargs__ ={
        '_keyword' : {'required':True},
        '_until': {'required':False,'default':None},
        '_since': {'required':False,'default':None},
        '_lang': {'required':False,'default':None},
        '_from': {'required':False,'default':None},
        '_df': {'required':False,'default':None},
        '_csv': {'required':False,'default':None},
        '_limit': {'required':False,'default':None},
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self, context=None):
        super().process()

        query = f"""{self._keyword} until:{self._until if self._until else None} 
                since:{self._since if self._since else None}
                lang:{self._lang if self._lang else None}
                from:{' OR '.join(self._from) if self._from else None}"""

        scraped_tweets = sntwitter.TwitterSearchScraper(query).get_items()
        if self._limit:
            sliced_scraped_tweets = scraped_tweets
        else:
            sliced_scraped_tweets = itertools.islice(scraped_tweets,self._limit)
            
        df = pd.DataFrame(sliced_scraped_tweets)

        if self._csv:
            df.to_csv(self._csv + '.csv', index=True,)

        return {self._df:df,'_res':f"Crawled {df.shape[0]} tweets"}


class CrawlerThreadExecutor(Pipe):

    __name__ = "Twitter Crawler Thread Executor"
    __kwargs__ ={
        '_keyword' : {'required':True},
        '_until': {'required':False,'default':None},
        '_since': {'required':False,'default':None},
        '_lang': {'required':False,'default':None},
        '_from': {'required':False,'default':None},
        '_df': {'required':False,'default':None},
        '_threads': {'required':False,'default':3},
        '_crawler': {'required':True}
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        with ThreadPoolExecutor(max_workers = self._threads) as executor:
            dates = [(date, date +  datetime.timedelta(days=1)) for date in pd.date_range(start=self._since,end=self._until,freq='D').date ]
            futures = {executor.submit(worker, self._crawler(_keyword=self._keyword,
                        _since=day_start,
                        _until=day_end,
                        _lang=self._lang,
                        _from=self._from,
                        _df=self._df
                    )) for (day_start,day_end) in dates}

            frames = []
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                frames.append(res[self._df])
            
            return {self._df: pd.concat(frames)}
    
def worker(crawler):
    return crawler.process()
