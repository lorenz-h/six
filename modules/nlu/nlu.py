import pickle

from ...spine.module_skeletons import InternalModule
from .parser import Parser

class NLUModule(InternalModule):

    name = "nlu"
    
    def __init__(self):
        self.parser = Parser()
        super(NLUModule, self).__init__()

    def on_msg(self, topic: str, message: bytes):
        if topic.endswith("/nlu/parse"):
            intent = self.parser.parse(message.decode("utf-8"))
            self.comm.publish(pickle.dumps(intent), "six/modules/nlu/intents")
