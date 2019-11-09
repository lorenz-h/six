import logging

from .utils import setup_console_output
from .spine import Spine
from .modules.mqtt import MQTTBrokerModule

if __name__ == "__main__":
    setup_console_output()
    sp = Spine()
    sp.add_module(MQTTBrokerModule)
    sp.loop()
