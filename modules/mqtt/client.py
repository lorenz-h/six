import time

import paho.mqtt.client as paho_mqtt

from spine.comm_skeletons import GenericCommInterface
from .mqtt import PORT, KEEPALIVE, WAIT_BEFORE_CONNECT

class MQTTInterface(GenericCommInterface):
    
    name = "mqtt_client"

    def __init__(self, topics, name, super_msg_callback):
        super(MQTTInterface, self).__init__(name)

        self.super_msg_callback = super_msg_callback

        self.client = paho_mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        

        self.topics = topics
    
    def _on_connect(self, client, userdata, flags, rc):
        
        self.logger.info("connected with result code "+str(rc))
        for topic in self.topics:
            self.subscribe(topic)
    
    def _on_message(self, client, userdata, msg):
        try:
            self.super_msg_callback(msg.topic, msg.payload)
        except Exception:
            self.logger.exception("MQTT Interface Message Callback Exeption")

    def subscribe(self, topic):
        if topic not in self.topics:
            self.topics.append(topic)
        self.client.subscribe(topic)

    def publish(self, msg, topic):
        self.client.publish(topic, msg)

    def start(self):
        time.sleep(WAIT_BEFORE_CONNECT)
        self.client.connect("localhost", PORT, KEEPALIVE)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()

