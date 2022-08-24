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
InGaAsMode = ('High Sensitivity', 'High Dynamic')
ModeValue = c_int(0)

# Temperature
Command1 = c_int(0x41)
Command2 = c_int(0x42)
ADValue = c_int(0)
DAChannel1 = 0
DAChannel2 = 1

setTemperature1 = c_double(0)
setTemperature2 = c_double(20)
getTemperature1 = c_double(0)
getTemperature2 = c_double(20)

detector_temperature_array = [-25]
chamber_temperature_array = [20]


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
        ttk.Label(root, text='device is initialized').place(x=250, y=10)
    else:
        ttk.Label(root, text='device initialization fails').place(x=250, y=10)


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

        ttk.Label(root, text=f'EEPROM reading is successful. Model is {Model}').place(x=250, y=40)
    else:
        ttk.Label(root, text='EEPROM reading fails').place(x=250, y=40)


def temperature_param_config(spmodel):
    global Command1
    global Command2
    # global DAChannel1
    # global DAChannel2
    if spmodel == 'BTC284N':
        Command1 = 0x41
        Command2 = 0x42

    elif spmodel == 'BTC281Y':
        Command1 = 0x61
        Command2 = 0x62


def TestUSB():
    isCommunicated = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
    if isCommunicated < 0:
        ttk.Label(root, text='Communication error').place(x=250, y=70)
    else:
        ttk.Label(root, text='Device timing mode {} and input mode {}'.format(TimingMode, InputMode)).place(x=250, y=70)


def getInGaAsMode():
    add_lib.bwtekGetInGaAsMode(byref(ModeValue), Channel)
    if ModeValue.value == 0:
        ttk.Label(root, text=f'InGaAs mode is high sensitivity').place(x=250, y=100)
    else:
        ttk.Label(root, text=f'InGaAs mode is high dynamic range').place(x=250, y=100)


def setIGAValue(event):
    global ModeValue
    selected_index = listbox.curselection()[0]
    if selected_index == 0:
        ModeValue = c_int(0)
    else:
        ModeValue = c_int(1)


def setInGaAsMode():
    add_lib.bwtekSetInGaAsMode(ModeValue, Channel)
    add_lib.bwtekGetInGaAsMode(byref(ModeValue), Channel)
    if ModeValue.value == 0:
        ttk.Label(root, text=f'InGaAs mode is high sensitivity').place(x=500, y=130)
    else:
        ttk.Label(root, text=f'InGaAs mode is high dynamic range').place(x=500, y=130)


def getTemperature_stage1():
    add_lib.bwtekReadTemperature(Command1, byref(ADValue), byref(getTemperature1), Channel)
    ttk.Label(root, text=f'Detector temperature is {getTemperature1.value}').place(x=250, y=160)


def getTemperature_stage2():
    add_lib.bwtekReadTemperature(Command2, byref(ADValue), byref(getTemperature2), Channel)
    ttk.Label(root, text=f'Chamber temperature is {getTemperature2.value}').place(x=250, y=190)


def setdetectortempvalue(event):
    global setTemperature1
    x = listbox_t1.curselection()[0]
    print(type(listbox_t1.get(x)))


def setchambertempvalue(event):
    global setTemperature2
    selected_index = listbox_t2.curselection()[0]
    if selected_index == 0:
        ModeValue = c_int(0)
    else:
        ModeValue = c_int(1)





def setTemperature_stage1():
    add_lib.bwtekSetTemperatureUSB(DAChannel1, setTemperature1, Channel)
    ttk.Label(root, text=f'Set temperature to{setTemperature1}').place(x=250, y=220)


def setTemperature_stage2():
    add_lib.bwtekSetTemperatureUSB(DAChannel2, setTemperature2, Channel)
    ttk.Label(root, text=f'Set Chamber temperature is{setTemperature2}').place(x=250, y=250)


dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)

root = tk.Tk()
root.title('SpectroTest')
root.geometry('800x600+50+50')
root.resizable(True, True)

# button_start = ttk.Button(root, text='Start')
# button_start.pack()
button_initialize = ttk.Button(root, text='Initialize spectrometer', width=30, command=initialization)
button_initialize.place(x=10, y=10)
# button_initialize.update_idletasks()

button_readEEPROM = ttk.Button(root, text='Read EEPROM', width=30, command=readEEPROM)
# button_readEEPROM.state(state)
button_readEEPROM.place(x=10, y=40)

# label_modelmatch = ttk.Label(root, text='Model matched')
# label_modelmatch.pack()

button_TestUSB = ttk.Button(root, text='Test USB', width=30, command=TestUSB)
button_TestUSB.place(x=10, y=70)


button_GetInGaAsMode = ttk.Button(root, text='Get InGaAs mode', width=30, command=getInGaAsMode)
button_GetInGaAsMode.place(x=10, y=100)

button_SetInGaAsMode = ttk.Button(root, text='Set InGaAs mode', width=30, command=setInGaAsMode)
button_SetInGaAsMode.place(x=10, y=130)

InGaAs = tk.StringVar(value=InGaAsMode)
listbox = tk.Listbox(root, listvariable=InGaAs, height=2, selectmode='browse')
listbox.place(x=250, y=130)
listbox.bind('<<ListboxSelect>>', setIGAValue)

button_readTemperature1 = ttk.Button(root, text='Read detector temperature', width=30, command=getTemperature_stage1)
button_readTemperature1.place(x=10, y=160)

button_readTemperature2 = ttk.Button(root, text='Read chamber temperature', width=30, command=getTemperature_stage2)
button_readTemperature2.place(x=10, y=190)

button_setTemperature1 = ttk.Button(root, text='Set detector temperature', width=30, command=setTemperature_stage1)
button_setTemperature1.place(x=10, y=220)

temp = tk.StringVar(value=detector_temperature_array)
listbox_t1 = tk.Listbox(root, listvariable=temp, height=5, selectmode='browse')
listbox_t1.place(x=250, y=220)
listbox_t1.bind('<<ListboxSelect>>', setdetectortempvalue)


button_setTemperature2 = ttk.Button(root, text='Set chamber temperature', width=30, command=setTemperature_stage2)
button_setTemperature2.place(x=10, y=350)
# button_setTemperature2.grid(padx=200, pady=50)

temp2 = tk.StringVar(value=chamber_temperature_array)
listbox_t2 = tk.Listbox(root, listvariable=temp2, height=5, selectmode='browse')
listbox_t2.place(x=250, y=350)
listbox_t2.bind('<<ListboxSelect>>', setchambertempvalue)


root.mainloop()