import time
import logging
from ...modules.mqtt import MQTTInterface as CommInterface

from .module import Module

class InternalModule(Module):

    name = "anon_internal_module"
    
    def __init__(self):
        super(InternalModule, self).__init__()
        topics = [f"six/modules/{self.name}/#"]
        self.logger.warning(f"{self.name} will subscribe to the topics: {topics}")
        self.comm = CommInterface(topics, f"{self.name}.comm", self.on_msg)

    def loop(self):
        self.comm.start()

        while True:
            time.sleep(5)
            self.hb.ping()

    def on_msg(self, topic: str, message: str):
        raise NotImplementedError("InternalModule is abstract")
        self.logger.warning(f"{topic} and {message}")
        

    def __del__(self):
        try:
            self.comm.stop()
        except Exception:
            logging.info("nlu module could not properly close communications.")
