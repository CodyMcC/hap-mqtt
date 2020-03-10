
from pyhap.accessory import Accessory

from pyhap.const import CATEGORY_LIGHTBULB

import paho.mqtt.client as mqtt

import logging

logger = logging.getLogger(__name__)


class BasicLight(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, location, mqtt_server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mqtt_server = mqtt_server
        self.client = mqtt.Client()
        self.client.connect(mqtt_server, 1883)
        self.topic = f"{self.location}/{self.display_name}/{self.aid}/Lightbulb"

        serv_light = self.add_preload_service('Lightbulb')

        self.char_on = serv_light.configure_char('On', setter_callback=self.set_bulb)
        self.set_info_service(firmware_revision=1, manufacturer="MonikerTechnology",
                              model="Alpha", serial_number=str(self.aid))

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_bulb(self, value):
        logger.info(f"{self.display_name} got an action: {value} [AID: {self.aid}]")
        value = '{"On": 0}'.replace("0", str(value))

        self.client.publish(self.topic, value)


