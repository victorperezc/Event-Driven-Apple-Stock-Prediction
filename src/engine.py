class PipelineEngine():

    def __init__(self,pipes,verbose=False):
        self._pipes = pipes
        self._verbose = verbose
        self._context = {}

    def process(self):
        print(f"[INFO] Starting Pipeline with {len(self._pipes)} pipes")
        for pipe in self._pipes:
            pipe.start()
            try:
                self._context = pipe.process(self._context)
                pipe.done()
                if '_res' in self._context:
                    print(f"  [RESULT] -> {self._context['_res']}")
                    del self._context['_res']
                
            except Exception as e:
                raise e
                pipe.error(e)
