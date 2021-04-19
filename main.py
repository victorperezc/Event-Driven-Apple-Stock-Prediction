from src.engine import PipelineEngine
from src.pipes.preprocessing import RemoveLinks
from src.pipes.crawler import TwitterCrawler,CrawlerThreadExecutor
from src.pipes.utils import TransformDataFrameColumn,TransformDataFrame,LoadDataFrame,SaveDataFrameToCsv,JoinDataFrame,ToDatetime
from src.pipes.openie import OpenIE
from src.pipes.encoders import BasicTextEncoder,TfIdf
from src.pipes.ml import MultiLayerPerceptron
from src.pipes.visualization import TimeSeries

PipelineEngine([
    TwitterCrawler(
        _keyword='Microsoft',
        _since='2010-01-01',
        _until='2019-01-01',
        _lang='en',
        _from=['CNN','cnnbrk','nytimes','BBCBreaking','TheEconomist'],
        _df='tweets',
        _csv='tweets'
    ),
    TransformDataFrameColumn(
        _transformation=RemoveLinks(),
        _df='tweets',
        _column='content'
    ),
    TransformDataFrame(
        _transformation=OpenIE(_keyword='Microsoft',_csv='embedded_tweets.csv'),
        _df='tweets',
    ),
    TransformDataFrame(
        _transformation=TfIdf(_csv='encoded_tweets.csv'),
        _df='tweets'
    ),
    TransformDataFrameColumn(
        _transformation=ToDatetime(),
        _df='tweets',
        _column='timestamp'
    ),
    SaveDataFrameToCsv(
        _df='tweets',
        _out='output.csv'
    ),
    LoadDataFrame(
        _name="msft_stock.csv",
        _alias='msft_stock'
    ),
    TransformDataFrameColumn(
        _transformation=ToDatetime(),
        _df='msft_stock',
        _column='timestamp'
    ),
    JoinDataFrame(
        _df1='tweets',
        _df2='msft_stock',
        _on='timestamp',
        _out='_data'
    ),
    MultiLayerPerceptron(
        _x_labels=['subject','object','relation','open','high','low','close','volume'],
        _y_labels=['class'],
        _df='_data',
        _hidden_layer_sizes=(100,50)
    ),
    MultiLayerPerceptron(
        _x_labels=['subject','object','relation','open','high','low','close','volume'],
        _y_labels=['class'],
        _df='_data',
        _hidden_layer_sizes=(50,25)
    ),
    MultiLayerPerceptron(
        _x_labels=['open','high','low','close','volume'],
        _y_labels=['class'],
        _df='_data',
        _hidden_layer_sizes=(100,50)
    ),
],verbose=True).process()