import logging

from spine import Spine
from modules.mqtt import MQTTBrokerModule
from modules.nlu import NLUModule

if __name__ == "__main__":
    sp = Spine()
    sp.add_module(MQTTBrokerModule)
    sp.add_module(NLUModule)
    sp.loop()
