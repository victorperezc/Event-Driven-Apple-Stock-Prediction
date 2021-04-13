from src.engine import PipelineEngine
from src.pipes.preprocessing import RemoveLinks
from src.pipes.crawler import TwitterCrawler,CrawlerThreadExecutor
from src.pipes.utils import TransformDataFrameColumn,TransformDataFrame,LoadDataFrame,SaveDataFrameToCsv,JoinDataFrame,ToDatetime
from src.pipes.openie import OpenIE
from src.pipes.encoders import BasicTextEncoder
from src.pipes.ml import MultiLayerPerceptron
from src.pipes.visualization import TimeSeries

PipelineEngine([
    LoadDataFrame(
        _name="embbeded_tweets.csv",
        _alias='tweets'
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