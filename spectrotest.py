import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from ctypes import *
import pandas as pd
from scipy.signal import savgol_filter as sg_smoothing
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from spectrotestfunctions import *

Channel = c_int(0)
# OutFileEEPROM = c_wchar_p('p')

SpectrometerType = 17
Model = ''
PixelNum = 512
TimingMode = c_int(1)
InputMode = c_int(2)
Param = c_int(0)

# InGaAs mode
ModeValue = c_int(0)

# Temperature
Command = c_int(0x41)
ADValue = c_int(0)
DAChannel = 0
Set_Temperature = c_double(0)
Read_Temperature = c_double(0)



xarray = np.arange(0, PixelNum, 1)


def parse_line(str_array):
    para = ''
    start = 0
    for character in str_array:
        if character == '=':
            start = 1
        else:
            if start == 0:
                continue
            elif character == '-':
                break
            else:
                para += character
    return para


def initialization():
    isInitialized = add_lib.InitDevices()
    if isInitialized:
        ttk.Label(root, text='device is initialized').pack(side='right')
    else:
        ttk.Label(root, text='device initialization fails').pack(side='right')


def readEEPROM():
    getEEPROM = add_lib.bwtekReadEEPROMUSB('p', Channel)
    global PixelNum
    global Model
    global SpectrometerType
    global TimingMode
    global InputMode
    if getEEPROM:
        with open('p') as file:
            for line in map(str.strip, file):
                if line.startswith('pixel_num'):
                    PixelNum = int(parse_line(line))
                elif line.startswith('model'):
                    Model = str(parse_line(line))
                elif line.startswith('spectrometer_type'):
                    SpectrometerType = int(parse_line(line))
                elif line.startswith('timing_mode'):
                    TimingMode = int(parse_line(line))
                elif line.startswith('input_mode'):
                    InputMode = int(parse_line(line))

        ttk.Label(root, text=f'EEPROM reading is successful. Model is {Model}').pack(side='left')
    else:
        ttk.Label(root, text='EEPROM reading fails').pack(side='left')


def model_match(spModel):
    global Command
    global ADValue
    global DAChannel
    if spModel == 'BTC284N':
        Command_stage1 = 0x41
        Command_stage2 = 0x42
        DAChannel_stage1 =
        DAChannel_stage2 =
    elif spModel == 'BTC281Y':




def TestUSB():
    isCommunicated = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
    if isCommunicated < 0:
        ttk.Label(root, text='Communication error').pack(side='left')
    else:
        ttk.Label(root, text='Device timing mode {} and input mode {}'.format(TimingMode, InputMode)).pack()


def getInGaAsMode():
    add_lib.bwtekGetInGaAsMode(byref(ModeValue), Channel)
    if ModeValue.value == 0:
        ttk.Label(root, text=f'InGaAs mode is high sensitivity').pack(side='left')
    else:
        ttk.Label(root, text=f'InGaAs mode is high dynamic range').pack(side='left')


def setInGaAsMode():
    add_lib.bwtekSetInGaAsMode(1, Channel)
    if ModeValue.value == 0:
        ttk.Label(root, text=f'InGaAs mode is high sensitivity').pack(side='left')
    else:
        ttk.Label(root, text=f'InGaAs mode is high dynamic range').pack(side='left')


def readTemperature1():
    add_lib.bwtekReadTemperature(Command, byref(ADValue), byref(Read_Temperature), Channel)


def readTemperature2():
    add_lib.bwtekReadTemperature(Command, byref(ADValue), byref(Read_Temperature), Channel)


def setTemperature1():
    add_lib.bwtekSetTemperatureUSB(DAChannel, Set_Temperature, Channel)


def setTemperature2():
    add_lib.bwtekSetTemperatureUSB(DAChannel, Set_Temperature, Channel)


dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)

root = tk.Tk()
root.title('SpectroTest')
root.geometry('800x600+50+50')
root.resizable(True, True)

# button_start = ttk.Button(root, text='Start')
# button_start.pack()
button_initialize = ttk.Button(root, text='Initialize spectrometer', command=initialization)
button_initialize.pack()

button_readEEPROM = ttk.Button(root, text='Read EEPROM', command=readEEPROM)
# button_readEEPROM.state(state)
button_readEEPROM.pack()

# label_modelmatch = ttk.Label(root, text='Model matched')
# label_modelmatch.pack()

button_TestUSB = ttk.Button(root, text='Test USB', command=TestUSB)
button_TestUSB.pack()

button_GetInGaAsMode = ttk.Button(root, text='Get InGaAs mode', command=getInGaAsMode)
button_GetInGaAsMode.pack()

button_SetInGaAsMode = ttk.Button(root, text='Set InGaAs mode', command=setInGaAsMode)
button_SetInGaAsMode.pack()

button_readTemperature1 = ttk.Button(root, text='Read detector temperature', command=readTemperature1)
button_readTemperature1.pack()

button_readTemperature2 = ttk.Button(root, text='Read chamber temperature', command=readTemperature2)
button_readTemperature2.pack()

button_setTemperature1 = ttk.Button(root, text='Set detector temperature', command=setTemperature1)
button_setTemperature1.pack()

button_setTemperature2 = ttk.Button(root, text='Set chamber temperature', command=setTemperature2)
button_setTemperature2.pack()



root.mainloop()