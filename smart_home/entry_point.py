from .actuating import DMX512
from .config import DMXConfig, ButtonsConfig
from .device import DimmableDevice, BinaryDevice
from .button_handler import ButtonFactory
from machine import Timer

class HomeService():

    def __init__(self):
        dmx_devices = []
        dmx_devices.append(DimmableDevice(1, 'kitchen'))
        dmx_devices.append(DimmableDevice(2, 'bedroom'))
        dmx_conf = DMXConfig()
        self.dmx = DMX512(config=dmx_conf, devices=dmx_devices)
        
        modbus_devices = []
        modbus_devices.append(BinaryDevice(0, 'bed_sophite'))
        modbus_devices.append(BinaryDevice(1, 'lamp'))
        #modbus_conf = ModbusConfig()
        #self.modbus = Mod
        
        btn_conf = ButtonsConfig()
        self.buttons = ButtonFactory(btn_conf)

        #self.dmx_poll = Timer(mode = Timer.PERIODIC, period = 2500, callback=self.dmx.service)