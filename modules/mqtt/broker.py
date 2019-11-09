from spine.module import ExternalModule

class MQTTBrokerModule(ExternalModule):
    
    name = "mqtt_broker"

    def __init__(self, port=8000):
        cmd ="mosquitto -p 8000"
        super(MQTTBrokerModule, self).__init__(cmd)

