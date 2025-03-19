#from abc import ABC
#from enum import Enum
#from .actuating import IInterface

class Rooms():
    TOWLET = 0
    SHOWER = 1
    KITCHEN = 2
    ROOM = 3
    BALCONY = 4
    HALL = 5

class IDevice():
    name : str
    channel : int
    room : Rooms
    #handler : IInterface
    on_value : int
    off_value : int
    
    def __init__(self, channel : int, name : str) -> None:
        self.channel = channel
        self.name = name
        
    def toggle(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass
    
    
class BinaryDevice(IDevice):
    pass 

class DimmableDevice(IDevice):
    brightless : int = 0 
    max_bright : int = 255
    min_bright : int = 0
    smooth : bool = False
    step_speed : int = 10
    
    def __init__(self, channel: int, name: str, brightless = 0, max_bright = 255, min_bright = 0, smooth = False, step_speed = 10) -> None:
        self.brightless = brightless
        self.max_bright = max_bright
        self.min_bright = min_bright
        self.smooth = smooth
        self.step_speed = step_speed
        super().__init__(channel, name)
    
    def toggle(self):
        if self.brightless > self.max_bright:
            self.brightless = self.min_bright
        elif self.brightless == self.min_bright:
            self.brightless = self.max_bright
    
    def turn_off(self):
        self.brightless = self.min_bright
    
    def turn_on(self):
        self.brightless = self.max_bright
    
    def set_brightless(self):
        pass

class LEDDevice(DimmableDevice):
    start_segment : int
    lenght : int
    effect : int #later
    
    def set_colour(self):
        pass 
    
    def set_fx(self):
        pass