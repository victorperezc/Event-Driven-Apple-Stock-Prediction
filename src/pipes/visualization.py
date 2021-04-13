import matplotlib.pyplot as plt
from .pipe import Pipe

class TimeSeries(Pipe):

    __name__ = "Time Series Visualization"
    __kwargs__ = {
        '_x': {'required':True},
        '_y': {'required':True},
        '_df': {'required':True},
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()

        context[self._df].plot(self._x,self._y)
        plt.show()

        return context
