# An Accessory mocking a temperature sensor.
# It changes its value every few seconds.
import random

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR
import paho.mqtt.client as mqtt


class TemperatureSensor(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, location, mqtt_server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.mqtt_server = mqtt_server
        self.client = mqtt.Client()
        self.client.on_publish = self.on_publish
        self.client.connect(mqtt_server, 1883)
        self.topic = f"{self.location}/{self.display_name}/{self.aid}/TemperatureSensor"

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

        self.set_info_service(firmware_revision=1, manufacturer="MonikerTechnology",
                              model="Alpha", serial_number=str(self.aid))

    def __setstate__(self, state):
        print("\n\n\t__setstate__ ran\n\n")
        self.__dict__.update(state)

    def __getstate__(self):
        print("\n\n\tgetting state __getstate__\n\n")
        state = super().__getstate__()
        # state['sensor'] = None

    def on_publish(self, client, userdata, mid):
        pass
        # print(client)
        # print(userdata)
        # print(mid)
