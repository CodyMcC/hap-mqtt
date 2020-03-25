import paho.mqtt.client as mqtt
from pyhap.accessory import Bridge, Accessory
import pyhap.loader as loader
from pyhap.const import CATEGORY_OTHER
from pyhap.accessory_driver import AccessoryDriver
import json

import logging

logger = logging.getLogger(__name__)



# get loaders
service_loader = loader.get_loader()
char_loader = loader.get_loader()


# class MqttAccessories:
#
#     accessories = []
#     topics = []
#
#     def __init__(self, accessory: Accessory):
#         self.name = accessory.display_name
#         self.aid = accessory.aid
#
#         self.accessory = accessory
#         for service in accessory.services:
#             MqttAccessories.topics.append(f"{self.name}/{self.aid}/{service.display_name}")
#             if service.display_name != "AccessoryInformation":
#                 self.service = service
#
#         self.topic = f"{self.name}/{self.aid}/{self.service}"
#
#         MqttAccessories.accessories.append(accessory)
#
#     def get_topic(self):
#         return self.topic


class HapMqtt(Bridge):
    category = CATEGORY_OTHER

    def __init__(self, mqtt_server, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = mqtt.Client()
        self.client.enable_logger()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(mqtt_server, 1883, 60)

        self.subscriptions = []
        self.topics = []


    # def add_accessory(self, acc, *args, **kwargs):
    #     super().__init__(acc.display_name, acc.driver)
    #
    #     if acc.topic not in self.topics:
    #         self.client.subscribe(acc.topic)
    #         self.topics.append(acc.topic)

    def add_topic(self, new_topic):
        if new_topic not in self.topics:
            logger.info(f"Subscribing to: %s", new_topic)
            self.client.subscribe(new_topic)
            self.topics.append(new_topic)

    def on_message(self, client, userdata, msg):
        logger.info("Topic: %s", msg.topic)
        logger.info("Msg: %s", msg.payload.decode())
        location = msg.topic.split("/")[0]
        name = msg.topic.split("/")[1]
        aid = int(msg.topic.split("/")[2])
        service = msg.topic.split("/")[3]

        # Prep payload from common issues
        msg.payload = msg.payload.decode()
        msg.payload = msg.payload.replace("\'", "\"")
        # TODO Add URL decode

        data = json.loads(msg.payload)

        logger.debug("Got %s", msg.topic)
        self.update_state(name, aid, service, data)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        logger.debug("Connected to mqtt server")

    def update_state(self, name, aid, service, data):
        """Update the characteristics from the received data.

        """

        logger.debug("Got update from accessory with aid: %d name %s", aid, name)
        accessory = self.accessories[aid]

        service_obj = accessory.get_service(service)

        for char, value in data.items():
            char_obj = service_obj.get_characteristic(char)
            # char_obj.client_update_value(value)  # Triggers the callback function
            char_obj.set_value(value)  # Only updates the value

    def run(self):
        print("\nstarting the loop\n")
        self.client.loop_forever()

    @Accessory.run_at_interval(2)
    def do(self):
        logger.info("Topic: asdfasdfalsjkdfhlasjkdfhlaksjdhflasjhdflasjhdflajshdflkajh")
        print("\nrunning the thing\n")

