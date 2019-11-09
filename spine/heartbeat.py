import logging

class HeartBeat:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger("six.heartbeat")
    
    def ping(self):
        self.logger.info(f"{self.name}: alive")