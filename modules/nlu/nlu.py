import time
from spine.module_skeletons import InternalModule

class NLUModule(InternalModule):

    name = "nlu"
    
    def __init__(self):
        super(NLUModule, self).__init__()
        
    def on_msg(self, topic: str, message: str):
        self.logger.warning(f"{topic} and {message}")
        