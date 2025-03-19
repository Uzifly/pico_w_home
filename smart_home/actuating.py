#from abc import ABC
from machine import Pin, Timer

from .utils import singleton
from lib.dmx_master import DMX
from .device import DimmableDevice
from .config import DMXConfig

from typing import Optional, Iterable, Union

class IInterface():
    name : str
    
    def health_check(self):
        pass
    
    def set_state(self, device, value) -> bool:
        return False
    
    def get_state(self, device) -> int:
        return 0
    
    def service(self):
        pass
    
@singleton
class DMX512(IInterface):
    UNIVERSE = 24
    __length = UNIVERSE #min universe message frame
    
    def __init__(self, config : DMXConfig, devices : list[DimmableDevice]):
        
        working_pin = config.dmx_pin
        if config.te is not None:
            pass
        self.length = len(devices)
        self.fps = config.fps
        self.devices = devices
        self.dmx = DMX(working_pin, size = self.length)
        # TODO Распаковка конфига и инициализация устройств
        
    @property
    def fps(self):
        return self.__fps
    
    @fps.setter
    def fps(self, var : int):
        
        self.__fps = 0
        
    @property
    def length(self):
        return self.__length
    
    @length.setter
    def length(self, var: int):
        if var > 512:
            self.__length = 512
        elif var < self.UNIVERSE:
            self.__length = self.UNIVERSE
        else:
            self.__length = var
            
    def get_state(self, device) -> int:
        return super().get_state(device)
    
    def service(self, t):
        for device in self.devices:
            self.dmx.universe[device.channel] = device.brightless
            print(f'send {self.dmx.universe}, t value = {t}')
            self.dmx.send()
    
    #def __smooth_dimming(self):
    #    self.step = 
    

@singleton
class Modbus(IInterface):
    def  __init__(self) -> None:
        pass
    
    
    
    
    
    

#@fabric ??
class RGBWLed(IInterface):
    pass