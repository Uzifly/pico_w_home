# Create a universe that we want to send.
# The universe must be maximum 512 bytes + 1 byte of start code

import time
from array import array
from typing import Optional

from machine import Pin
from rp2 import StateMachine
# -----------------------------------------------
# add type hints for the rp2.PIO Instructions
from typing_extensions import TYPE_CHECKING

from pio_code.pio_dmx import dmx_receive, dmx_send

class DMX:
    """
    DMX class for controlling DMX universe.

    Args:
        dmx_tx (Pin): The pin used for transmitting DMX data.
        size (int, optional): The size of the DMX universe. Defaults to 512.
        max485_send (Optional[Pin], optional): The pin used for controlling the MAX485 chip. Defaults to None.

    Attributes:
        universe (array): The DMX universe array.
        sm_tx (StateMachine): The state machine for transmitting DMX data.
        max485_send (Optional[Pin]): The pin used for controlling the MAX485 chip.

    Methods:
        send: Send the universe to the DMX bus.
        set_channel: Set the value of a specific DMX channel.
        get_channel: Get the value of a specific DMX channel.
        blackout: Set all channels to 0.
    """
    
    def __init__(self, dmx_tx: Pin , size:int = 512, max485_send: Optional[Pin] = None):
        self.universe = array("B", [0] + [0] * (size))  # 1 start code + 512 channels
        machine_nr = 0
        self.max485_send = max485_send
        self.sm_tx = StateMachine(
            machine_nr,
            dmx_send,
            freq=1_000_000,
            out_base=dmx_tx,
            sideset_base=dmx_tx,
        )

    def set_channel(self, channel: int, value: int):
        """
        Set the value of a specific DMX channel.

        Args:
            channel (int): The channel number.
            value (int): The value to set.
        """
        self.universe[channel] = value


    def get_channel(self, channel: int):
        """
        Get the value of a specific DMX channel.

        Args:
            channel (int): The channel number.

        Returns:
            int: The value of the channel.
        """
        return self.universe[channel]

    def set_all(value : int = 0):
        """
        Set all channels to 0.
        """	
        for i in range(1, len(self.universe)):
            self.universe[i] = value


    def send(self):
        """
        Send the universe to the DMX bus.
        """	
        if self.max485_send:
            self.max485_send.on()  # switch the MAX485 chip for transmitting
        self.sm_tx.restart()
        self.sm_tx.active(1)
        self.sm_tx.put(self.universe) 
        if self.max485_send:
            while (self.sm_tx.tx_fifo() != 0):
                time.sleep_us(50)  # wait for the last 4 frames (4 x 44us and some) in the tx FIFO to be sent before switching the 485 driver
            self.max485_send.off()  # switch the MAX485 chip for receiving


