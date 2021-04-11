from .pipe import Pipe
import re
class RemoveLinks(Pipe):
    
    __name__ = "Remove Links"
    __kwargs__ = {}

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,context):
        super().process()

        return {
            '_data':  [ re.sub(r'http\S+', '', item) for item in context['_data'] ] 
        }
    
    @property
    def allowed_keys(self):
        return {'_data'}
