from .config import ButtonsConfig
from lib.button import Button
from machine import Pin
from typing import Dict
import time
from collections import deque
import sys

class EVENT_TYPES:
    pressed = 'pressed'
    released = 'released' 
    click = 'click'
    longpress = 'longpress' 
    multiclick = 'multiclick'

class Event():
    e_types = []
    e_type = None
    count = 0
    actions = {}
    
    def __init__(self, config : dict) -> None:
        self.actions = config

class ClickCounter:
    __count = 0
    __event_ts = sys.maxsize
    
    def __init__(self, threshold) -> None:
        self.threshold = threshold
    
    @property
    def count(self):
        cnt = self.__count
        self.__count = 0
        self.__event_ts = sys.maxsize
        return cnt
    
    @count.setter
    def count(self, value : int):
        self.__count = value
        self.__event_ts = time.ticks_ms()
        
    def __eq__(self, other) -> bool:
        return self.__event_ts == other - self.threshold
    
    def __lt__(self, other) -> bool:
        return self.__event_ts < other - self.threshold
    
    def __gt__(self, other) -> bool:
        return self.__event_ts > other - self.threshold
    
    
class ButtonEvents(Button):
    def __init__(self, 
                 pin, 
                 name : str, 
                 callback,
                 rest_state=False,
                 internal_pullup=False, 
                 internal_pulldown=False, 
                 debounce_time_ms=None,
                 LP_THRESHOLD = 1000,
                 BP_THRESHOLD = 400):
        
        self.LP_THRESHOLD = LP_THRESHOLD #theshold in ms between press and longpress
        
        self.action = callback
        self.name = name
        self.click_type = ['none', time.ticks_ms()]
        self.click_counter = ClickCounter(BP_THRESHOLD)
        self.events = deque((), 10)
        
        super().__init__(pin, rest_state, None, internal_pullup, internal_pulldown, debounce_time_ms)
        
    def update(self, *args, **kwargs):
        event = self.handle_events()
        self.last_event = None
        if event:
            self.generate_event(event)

            self.__switch_handler(event)
        self.__multiclick_handler()
        self.__long_press_handler()
        if self.events:
            self.call_callback(self.events.popleft(), *args, **kwargs)
        
    def __switch_handler(self, btn_status):
        if btn_status == self.PRESSED:
            self.click_type = ['single', time.ticks_ms()]
            
        if btn_status == self.RELEASED:
            self.click_type = ['released', time.ticks_ms()]

        if self.click_type is not None and self.click_type[0] == 'single':
            self.click_counter.count += 1
            #self.click_counter[1] = time.ticks_ms()
            self.generate_event(EVENT_TYPES.click) 
    
    def __multiclick_handler(self):
        if self.click_counter < time.ticks_ms() and self.click_type[0] == 'released':
            self.generate_event((EVENT_TYPES.multiclick, self.click_counter.count))
    
    def __long_press_handler(self):
        probe_ts = time.ticks_ms()
        if self.click_type[0] == 'single' and (probe_ts - self.click_type[1]) > self.LP_THRESHOLD :
            self.click_type[0] = 'longpress'
            self.generate_event(EVENT_TYPES.longpress)
            self.click_counter.count #reset multiclick counter
            
    def generate_event(self, event_name):
        self.events.append(event_name)
        
    def call_callback(self, *args, **kwgs):
        if self.action:
            self.action(*args, **kwgs)
    

class ButtonFactory():
    def __init__(self, config : ButtonsConfig) -> None:
        PULLUP = 'Up'
        PULLDOWN = 'Down'
        LP_THRESHOLD = 1000 #theshold in ms between press and longpress
        BP_THRESHOLD = 400 #theshold in ms between release and press in multiclick event
        
        self.buttons : Dict[str, Button] = {}
        for btn in config.buttons:
            pullup = False
            pulldown = False
            if btn['pull'] == PULLUP:
                pullup = True
            elif btn['pull'] == PULLDOWN:
                pulldown = True
            self.buttons[btn['name']] = \
                ButtonEvents(
                    btn['pin'],
                    btn['name'],
                    lambda x, y : print(x, y),
                    btn['rest'],
                    internal_pulldown=pulldown,
                    internal_pullup=pullup,
                    debounce_time_ms=None,
                    LP_THRESHOLD=LP_THRESHOLD,
                    BP_THRESHOLD=BP_THRESHOLD)
                
    
    def service(self):
        for name, btn in self.buttons.items():
            btn.update(name)