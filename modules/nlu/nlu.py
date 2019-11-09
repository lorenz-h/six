import time
from modules.mqtt import MQTTInterface as CommInterface
from spine.module import Module

class NLUModule(Module):

    name = "nlu"
    
    def __init__(self):
        super(NLUModule, self).__init__()
        self.comm = CommInterface(["six/nlu/#"], "nlu.comm", self.on_msg)

    def loop(self):
        self.comm.start()

        while True:
            time.sleep(5)
            self.hb.ping()

    def on_msg(self, topic: str, message: str):
        self.logger.warning(f"{topic} and {message}")
        

    def __del__(self):
        try:
            self.comm.stop()
        except Exception:
            logging.info("nlu module could not properly close communications.")
