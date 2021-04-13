from .pipe import Pipe
import pandas as pd

class TransformDataFrame(Pipe):
    __name__ = "Data Frame Transformation"
    __kwargs__ = {
        '_transformation' : {'required':True},
        '_df' : {'required':True},
    }
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()

        context[self._df] = self._transformation.process(
            {'_data':context[self._df]}
        )['_data']

        return context

class TransformDataFrameColumn(Pipe):
    
    __name__ = "Data Frame Column Transformation"
    __kwargs__ = {
        '_column' : {'required':True},
        '_transformation' : {'required':True},
        '_df' : {'required':True},
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()

        context[self._df][self._column] = self._transformation.process(
            {'_data':context[self._df][self._column].to_list()}
        )['_data']

        return context

class LoadDataFrame(Pipe):

    __name__ = "Data Frame Loader"
    __kwargs__ = {
        '_name' : {'required':True},
        '_alias' : {'required':True}
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        if self._alias:
            context[self._alias] = pd.read_csv(self._name)
        else:
            context[self._name] = pd.read_csv(self._name)
        return context
    
class SaveDataFrameToCsv(Pipe):
    
    __name__ = "Data Frame Saver to CSV"
    __kwargs__ = {
        '_df' : {'required':True},
        '_out' : {'required':True}
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        context[self._df].to_csv(self._out,index=False)

        return context

class ToDatetime(Pipe):
    
    __name__ = "Data Frame Saver to CSV"
    __kwargs__ = {}

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        context['_data'] = pd.to_datetime(context['_data'])

        return context

class JoinDataFrame(Pipe):

    __name__ = "Join Data Frame"
    __kwargs__ = {
        '_df1' : {'required':True},
        '_df2' : {'required':True},
        '_on' : {'required':True},
        '_out' : {'required':True},
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        context[self._out] = pd.merge_asof(context[self._df1].sort_values('timestamp'), context[self._df2].sort_values('timestamp'), on='timestamp')
        
        return context
