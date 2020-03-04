from pyhap.accessory_driver import AccessoryDriver
from hap_mqtt import MqttAccessories, HapMqtt
import signal
import logging
from os.path import expanduser


from accessories.temperature_sensor import TemperatureSensor
from accessories.basic_light import BasicLight

accessory_state = expanduser('~/Documents/2. Code/2. Python/HAP-MQTT/accessory.state')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(module)-16s] [%(levelname)-8s] %(message)s",
                    datefmt="%I:%M:%S %p")

# Start the accessory on port 51826
driver = AccessoryDriver(port=51827,
                         persist_file=accessory_state)

mqtt_bridge = HapMqtt(driver, "mqtt_bridge")

# Create accessories
MqttAccessories("Outside", BasicLight(driver, "different", aid=999399))
MqttAccessories("Outside", BasicLight(driver, "Flood_1", aid=1234))
MqttAccessories("Garage", TemperatureSensor(driver, "Battery_1", aid=2323))


# Add the accessories and the topics to the mqtt bridge
for acc in MqttAccessories.accessories:
    mqtt_bridge.add_accessory(acc)
for topic in MqttAccessories.topics:
    mqtt_bridge.add_topic(topic)

driver.add_accessory(accessory=mqtt_bridge)

signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()

