
from pyhap.accessory import Accessory

from pyhap.const import CATEGORY_SENSOR

import logging

logger = logging.getLogger(__name__)


class TemperatureSensor(Accessory):
    """"""

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature', setter_callback=self.update)

    def update(self, value):
        logger.info(f"{self.display_name} got an action: {value} [AID: {self.aid}]")
