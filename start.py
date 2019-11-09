import logging

from spine import Spine
from modules.mqtt import MQTTBrokerModule

if __name__ == "__main__":
    sp = Spine()
    sp.add_module(MQTTBrokerModule)
    sp.loop()
