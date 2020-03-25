from pyhap.accessory_driver import AccessoryDriver
from hap_mqtt import HapMqtt
from pyhap.accessory import Accessory
import pyhap.loader as loader
import signal
import logging
from os.path import expanduser

from accessories.basic_light import BasicLight
from accessories.temperature_sensor import TemperatureSensor
from accessories.temp_sensor import TemperatureSensor

MQTTSERVER = "pi-server"
accessory_state = expanduser('~/github/hap-mqtt/accessory.state')

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

accessories = list()
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_1", aid=1111))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_2", aid=1222))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_3", aid=1333))
accessories.append(BasicLight("outside", MQTTSERVER, driver, "flood_4", aid=1444))

accessories.append(TemperatureSensor("garage", MQTTSERVER, driver, "battery_1", aid=2111))
accessories.append(TemperatureSensor("garage", MQTTSERVER, driver, "battery_2", aid=2222))
accessories.append(TemperatureSensor("garage", MQTTSERVER, driver, "battery_3", aid=2333))
accessories.append(TemperatureSensor("garage", MQTTSERVER, driver, "ambient", aid=2444))

# accessories.append(TemperatureSensor(driver, "fake_temp"))


# accessories.append(test)
# MqttAccessories(TemperatureSensor(MQTTSERVER, driver, "Battery_1", aid=2323))
# MqttAccessories.accessories[2].add_service(service_loader.get_service("BatteryService"))


# Add the accessories and the topics to the mqtt bridge
for acc in accessories:
    mqtt_bridge.add_accessory(acc)
    try:
        mqtt_bridge.add_topic(acc.topic)
    except AttributeError:
        pass


driver.add_accessory(accessory=mqtt_bridge)
# driver.add_accessory(accessory=TemperatureSensor(driver, "fake_temp"))

signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()

