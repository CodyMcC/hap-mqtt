
from pyhap.accessory import Accessory

from pyhap.const import CATEGORY_LIGHTBULB

import logging

logger = logging.getLogger(__name__)


class BasicLight(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, *args, pin=11, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char('On', setter_callback=self.set_bulb)

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_bulb(self, value):
        logger.info(f"{self.display_name} got an action: {value} [AID: {self.aid}]")
