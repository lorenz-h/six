import logging

from ..heartbeat import HeartBeat

class GenericCommInterface:
    """
    This class is used to provide a layer of abstraction for spine.modules to use a communiation protocol such as mqtt.
    The client implementation for the protocol should inherit this class.
    """

    name = "generic_comm_interface"

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(f"six.modules.{self.name}")
        self.hb = HeartBeat(self.name)

    def publish(self, msg, topic):
        raise NotImplementedError()
    
    def subscribe(self, topic):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()
    
    def stop(self):
        raise NotImplementedError()
