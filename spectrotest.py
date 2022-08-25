import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from ctypes import *
# import pandas as pd
# from scipy.signal import savgol_filter as sg_smoothing
# from scipy import interpolate
import numpy as np
# import matplotlib.pyplot as plt
# import time
# import os
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
modelwith2stagecooling = ['BTC284N', 'BTC281Y']
modelwithCDC = ['BTC284N', 'BTC281Y']


def initialization():
    label_initialize = ttk.Label(root, text='')
    label_initialize.place(x=250, y=10)
    isInitialized = add_lib.InitDevices()
    global button_readEEPROM
    if isInitialized:
        button_initialize['text'] = 'device is initialized'
        button_readEEPROM['state'] = 'normal'
    else:
        button_initialize['text'] = 'device initialization fails'
        button_readEEPROM['state'] = 'disabled'


def readEEPROM():
    getEEPROM = add_lib.bwtekReadEEPROMUSB('para.ini', Channel)
    global PixelNum
    global Model
    global SpectrometerType
    global TimingMode
    global InputMode
    global button_TestUSB
    label_EEPROM = ttk.Label(root)
    label_EEPROM.place(x=250, y=40)
    if getEEPROM > 0:
        button_TestUSB['state'] = 'normal'
        PixelNum = getPixelNumfromEEPROM('p')
        Model = getModelfromEEPROM('p')
        SpectrometerType = getSPTypefromEEPROM('p')
        TimingMode = getTimingModefromEEPROM('p')
        InputMode = getInputModefromEEPROM('p')
        temperature_param_config(Model)
        label_EEPROM.config(text=f'EEPROM reading is successful. Model is {Model}')
    else:
        button_TestUSB['state'] = 'disabled'
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


def testUSB():
    label_testUSB = ttk.Label(root, text='Setting Communication')
    label_testUSB.place(x=250, y=70)
    isCommunicated = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
    global button_GetInGaAsMode
    global button_SetInGaAsMode
    if isCommunicated < 0:
        label_testUSB['text'] = 'Communication error'
    else:
        label_testUSB['text'] = 'Device is ready'
        if Model.startswith('BTC26') or Model.startswith('BTC28'):
            button_GetInGaAsMode['state'] = 'normal'
            button_SetInGaAsMode['state'] = 'normal'
            listbox_IGA.place(x=250, y=130)
        if Model in modelwith2stagecooling:
            button_readTemperature1['state'] = 'normal'
            button_readTemperature2['state'] = 'normal'
            button_setTemperature1['state'] = 'normal'
            button_setTemperature2['state'] = 'normal'


def getInGaAsMode():
    label_getIGA = ttk.Label(root, text='Getting InGaAs mode')
    label_getIGA.place(x=250, y=100)
    add_lib.bwtekGetInGaAsMode(byref(ModeValue), Channel)
    if ModeValue.value == 0:
        label_getIGA['text'] = 'InGaAs mode is high sensitivity'
    elif ModeValue.value == 1:
        label_getIGA['text'] = 'InGaAs mode is high dynamic range'
    else:
        label_getIGA['text'] = 'unable to get InGaAs working mode'


def setIGAValue(event):
    global ModeValue
    selected_index = listbox_IGA.curselection()[0]
    if selected_index == 0:
        ModeValue = c_int(0)
    else:
        ModeValue = c_int(1)


def setInGaAsMode():
    label_setIGA = ttk.Label(root, text='Setting InGaAs mode')
    label_setIGA.place(x=500, y=130)
    add_lib.bwtekSetInGaAsMode(ModeValue, Channel)
    add_lib.bwtekGetInGaAsMode(byref(ModeValue), Channel)
    if ModeValue.value == 0:
        label_setIGA['text'] = 'InGaAs mode is high sensitivity'
    else:
        label_setIGA['text'] = 'InGaAs mode is high dynamic range'


def getTemperature_stage1():
    add_lib.bwtekReadTemperature(Command1, byref(ADValue), byref(getTemperature1), Channel)
    ttk.Label(root, text=f'Detector temperature is {getTemperature1.value}').place(x=250, y=160)


def getTemperature_stage2():
    add_lib.bwtekReadTemperature(Command2, byref(ADValue), byref(getTemperature2), Channel)
    ttk.Label(root, text=f'Chamber temperature is {getTemperature2.value}').place(x=250, y=190)


def setDetectortempvalue(event):
    global setTemperature1
    x = listbox_t1.curselection()[0]
    print(type(listbox_t1.get(x)))


def setChambertempvalue(event):
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

button_readEEPROM = ttk.Button(root, text='Read EEPROM', state='disabled', width=30, command=readEEPROM)
# button_readEEPROM.state(state)
button_readEEPROM.place(x=10, y=40)

# label_modelmatch = ttk.Label(root, text='Model matched')
# label_modelmatch.pack()

button_TestUSB = ttk.Button(root, text='Test USB', state='disabled', width=30, command=testUSB)
button_TestUSB.place(x=10, y=70)

button_GetInGaAsMode = ttk.Button(root, text='Get InGaAs mode', state='disabled', width=30, command=getInGaAsMode)
button_GetInGaAsMode.place(x=10, y=100)

button_SetInGaAsMode = ttk.Button(root, text='Set InGaAs mode', state='disabled', width=30, command=setInGaAsMode)
button_SetInGaAsMode.place(x=10, y=130)

InGaAs = tk.StringVar(value=InGaAsMode)
listbox_IGA = tk.Listbox(root, listvariable=InGaAs, height=2, selectmode='browse')
# listbox_IGA.place(x=250, y=130)
listbox_IGA.bind('<<ListboxSelect>>', setIGAValue)

button_readTemperature1 = ttk.Button(root, text='Read detector temperature', state='disabled', width=30,
                                     command=getTemperature_stage1)
button_readTemperature1.place(x=10, y=160)

button_readTemperature2 = ttk.Button(root, text='Read chamber temperature', state='disabled', width=30,
                                     command=getTemperature_stage2)
button_readTemperature2.place(x=10, y=190)

button_setTemperature1 = ttk.Button(root, text='Set detector temperature', state='disabled', width=30,
                                    command=setTemperature_stage1)
button_setTemperature1.place(x=10, y=220)

temp1 = tk.StringVar(value=detector_temperature_array)
listbox_t1 = tk.Listbox(root, listvariable=temp1, height=5, selectmode='browse')
listbox_t1.place(x=250, y=220)
listbox_t1.bind('<<ListboxSelect>>', setDetectortempvalue)

button_setTemperature2 = ttk.Button(root, text='Set chamber temperature', state='disabled', width=30,
                                    command=setTemperature_stage2)
button_setTemperature2.place(x=10, y=350)
# button_setTemperature2.grid(padx=200, pady=50)

temp2 = tk.StringVar(value=chamber_temperature_array)
listbox_t2 = tk.Listbox(root, listvariable=temp2, height=5, selectmode='browse')
listbox_t2.place(x=250, y=350)
listbox_t2.bind('<<ListboxSelect>>', setChambertempvalue)

root.mainloop()
