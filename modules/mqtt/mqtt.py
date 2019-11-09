from ...spine.module import ExternalModule


class MQTTBrokerModule(ExternalModule):
    def __init__(self, port=8000):
        cmd ="mosquitto -p 8000"
        super(MQTTBrokerModule, self).__init__("mqtt_broker", cmd)

    

class MQTTClient:
    def __init__():
        raise NotImplementedError()