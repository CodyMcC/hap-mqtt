from pyhap.accessory_driver import AccessoryDriver
from hap_mqtt import HapMqtt
from pyhap.accessory import Accessory
import pyhap.loader as loader
import signal
import logging
from os.path import expanduser


from accessories.temperature_sensor import TemperatureSensor
from accessories.basic_light import BasicLight


MQTTSERVER = "192.168.1.132"
accessory_state = expanduser('~/Documents/2. Code/2. Python/HAP-MQTT/accessory.state')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(module)-16s] [%(levelname)-8s] %(message)s",
                    datefmt="%I:%M:%S %p")

# Start the accessory on port 51826
driver = AccessoryDriver(port=51827,
                         persist_file=accessory_state)

mqtt_bridge = HapMqtt(MQTTSERVER, driver, "mqtt_bridge")


# get loaders
service_loader = loader.get_loader()
char_loader = loader.get_loader()

test = Accessory(driver, "Switch", aid=999196)
test.add_service(service_loader.get_service("Switch"))
# MqttAccessories(test)
# mqtt_bridge.add_accessory(test)

# Create accessories
# MqttAccessories("Outside", BasicLight(driver, "different", aid=999399))
# MqttAccessories(BasicLight("outside", MQTTSERVER, driver, "flood_1", aid=1111))
# MqttAccessories(BasicLight("outside", MQTTSERVER, driver, "flood_2", aid=2222))
# MqttAccessories(BasicLight("outside", MQTTSERVER, driver, "flood_3", aid=3333))
# MqttAccessories(BasicLight("outside", MQTTSERVER, driver, "flood_4", aid=4444))

accessories = list()
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_1", aid=1111))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_2", aid=2222))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_3", aid=3333))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_4", aid=4444))
# MqttAccessories(TemperatureSensor(MQTTSERVER, driver, "Battery_1", aid=2323))
# MqttAccessories.accessories[2].add_service(service_loader.get_service("BatteryService"))


# Add the accessories and the topics to the mqtt bridge
for acc in accessories:
    mqtt_bridge.add_accessory(acc)
    mqtt_bridge.add_topic(acc.topic)
# for topic in MqttAccessories.topics:
#     mqtt_bridge.add_topic(topic)



driver.add_accessory(accessory=mqtt_bridge)

signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()

