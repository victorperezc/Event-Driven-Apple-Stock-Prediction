from .pipe import Pipe
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class MultiLayerPerceptron(Pipe):
    
    __name__ = "Multi Layer Perceptron"
    __kwargs__ = {
        '_x_labels': {'required':True},
        '_y_labels': {'required':True},
        '_df': {'required':True},
        '_hidden_layer_sizes':{'required':True}
    }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()
        X = context[self._df][self._x_labels]
        y = context[self._df][self._y_labels]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        pipe = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=self._hidden_layer_sizes))
        pipe.fit(X_train, y_train)  # apply scaling on training data
        pipe.score(X_test, y_test)  # apply scaling on testing data, without leaking training data.
        return {'_res':f"R^2: {pipe.score(X_test, y_test)}"}

