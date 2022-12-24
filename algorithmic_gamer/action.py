# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_action.ipynb.

# %% auto 0
__all__ = ['send_input']

# %% ../nbs/02_action.ipynb 1
from .types import *
from .fuzzer import *
import ctypes
import time

# %% ../nbs/02_action.ipynb 2
#|eval: false
####TODO test further
def send_input(input_dict):
    # Set the default values for the input values
    x = 0
    y = 0
    trigger_left = 0
    trigger_right = 0
    wButtons = 0

    # Parse the input dictionary
    for key, value in input_dict.items():
        if key == "stick":
            x = int(32767 * value["x"])
            y = int(32767 * value["y"])
        elif key == "trigger":
            if value["side"] == "left":
                trigger_left = int(32767 * value["v"])
            elif value["side"] == "right":
                trigger_right = int(32767 * value["v"])
        elif key == "button":
            if value["state"] == "press":
                if value["name"] == "A":
                    wButtons |= 0x1000
                elif value["name"] == "B":
                    wButtons |= 0x2000
                elif value["name"] == "X":
                    wButtons |= 0x4000
                elif value["name"] == "Y":
                    wButtons |= 0x8000
                elif value["name"] == "LEFT_SHOULDER":
                    wButtons |= 0x0100
                elif value["name"] == "RIGHT_SHOULDER":
                    wButtons |= 0x0200
                elif value["name"] == "BACK":
                    wButtons |= 0x0400
                elif value["name"] == "START":
                    wButtons |= 0x0800
                elif value["name"] == "LEFT_THUMB":
                    wButtons |= 0x0010
                elif value["name"] == "RIGHT_THUMB":
                    wButtons |= 0x0020

    # Create the input structure
    class INPUT(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ki", ctypes.c_ulonglong),
                    ("hi", ctypes.c_ulonglong),
                    ("mi", ctypes.c_ulonglong),
                    ("gp", ctypes.c_ulonglong)]
    input_structure = INPUT(type=2,
                            ki=0,
                            hi=0,
                            mi=0,
                            gp=x | y << 16 | trigger_left << 32 | trigger_right << 48 | wButtons << 16)

    # Send the input
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_structure), ctypes.sizeof(input_structure))

