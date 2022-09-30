import tkinter as tk
from tkinter import ttk
# from tkinter.messagebox import showinfo
from ctypes import *
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time
from spectrotestfunctions import *


def setInterface():
    pass
    # TT = interfaceType.get()
    # global InterfaceType
    # InterfaceType = int(TT) - 1
    # print(f'Interface type is {InterfaceTypes[InterfaceType]}')
    # if InterfaceType == 0:
    #     button_Test['text'] = 'TestUSB'
    #     button_initialize['state'] = 'normal'
    # elif InterfaceType == 1:
    #     button_Test['text'] = 'TestRS232'
    #     button_initialize['state'] = 'normal'
    # else:
    #     button_Test['text'] = 'TestNull'
    #     button_initialize['state'] = 'disabled'


root = tk.Tk()
root.title('SpectroTest')
root.geometry('1200x900+50+50')
root.resizable(True, True)

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Functions Test')
tabControl.add(tab2, text='Channel Difference Calibration')
tabControl.pack(expand=1, fill="both")

interfaceType = tk.StringVar()
radio_interface_USB = ttk.Radiobutton(tab1, text='USB', variable=interfaceType, value=1, command=setInterface)
radio_interface_RS232 = ttk.Radiobutton(tab1, text='RS232', variable=interfaceType, value=2, command=setInterface)
radio_interface_OTHERS = ttk.Radiobutton(tab1, text='Others', variable=interfaceType, value=3, command=setInterface)
radio_interface_USB.place(x=250, y=10)
radio_interface_RS232.place(x=350, y=10)
radio_interface_OTHERS.place(x=450, y=10)

label_comPort = ttk.Label(tab1, text='COM port')
label_comPort.place(x=550, y=10)
comPort = tk.StringVar()
textbox_comport = ttk.Entry(tab1, text='', textvariable=comPort, width=10)
textbox_comport.place(x=650, y=10)
#
# button_initialize = ttk.Button(root, text='Initialize spectrometer', state='disabled', width=30, command=initialization)
# button_initialize.place(x=10, y=40)
#
# button_readEEPROM = ttk.Button(root, text='Read EEPROM', state='disabled', width=30, command=readEEPROM)
# button_readEEPROM.place(x=10, y=70)
#
# label_test = ttk.Label(root, text='')
# button_Test = ttk.Button(root, text='Test', state='disabled', width=30, command=test)
# button_Test.place(x=10, y=100)
#
# button_GetInGaAsMode = ttk.Button(root, text='Get InGaAs mode', state='disabled', width=30, command=getInGaAsMode)
# button_GetInGaAsMode.place(x=10, y=130)
#
# button_SetInGaAsMode = ttk.Button(root, text='Set InGaAs mode', state='disabled', width=30, command=setInGaAsMode)
# button_SetInGaAsMode.place(x=10, y=160)
#
# InGaAs = tk.StringVar(value=InGaAsMode)
# listbox_IGA = tk.Listbox(root, listvariable=InGaAs, height=2, selectmode='browse')
# listbox_IGA.bind('<<ListboxSelect>>', setIGAValue)
#
# button_readTemperature1 = ttk.Button(root, text='Read detector temperature', state='disabled', width=30,
#                                      command=getTemperature_stage1)
# button_readTemperature1.place(x=10, y=190)
#
# button_readTemperature2 = ttk.Button(root, text='Read chamber temperature', state='disabled', width=30,
#                                      command=getTemperature_stage2)
# button_readTemperature2.place(x=10, y=220)
#
# button_setTemperature1 = ttk.Button(root, text='Set detector temperature', state='disabled', width=30,
#                                     command=setTemperature_stage1)
# button_setTemperature1.place(x=10, y=250)
#
# label_setDetectorT = ttk.Label(root, text='Detector T (-25 to 0)')
# setDetectorT = tk.StringVar()
# textbox_setDetectorTemp = ttk.Entry(root, textvariable=setDetectorT, width=10)
# textbox_setDetectorTemp.insert(0, '-25')
#
# button_setTemperature2 = ttk.Button(root, text='Set chamber temperature', state='disabled', width=30,
#                                     command=setTemperature_stage2)
# button_setTemperature2.place(x=10, y=280)
#
# label_setChamberT = ttk.Label(root, text='Chamber T (10 to 30)')
# setChamberT = tk.StringVar()
# textbox_setChamberTemp = ttk.Entry(root, textvariable=setChamberT, width=10)
# textbox_setChamberTemp.insert(0, '20')
#
# label_gain = ttk.Label(root, text='Gain (0-65535)')
# gaintext = tk.StringVar()
# textbox_gain = ttk.Entry(root, textvariable=gaintext, width='10')
# textbox_gain.insert(0, '10000')
#
# label_offset = ttk.Label(root, text='Offset (0-4095)')
# offsettext = tk.StringVar()
# textbox_offset = ttk.Entry(root, textvariable=offsettext, width='10')
# textbox_offset.insert(0, '100')
#
# button_readGain_Offset = ttk.Button(root, text='Read Gain and Offset', state='disabled', width=30,
#                                     command=getGainOffset)
# button_readGain_Offset.place(x=10, y=310)
#
# button_setGain_Offset = ttk.Button(root, text='Set Gain and Offset', state='disabled', width=30,
#                                    command=setGainOffset)
# button_setGain_Offset.place(x=10, y=340)
#
# label_inttime = ttk.Label(root, text='Integration time (ms)')
# inttimetext = tk.StringVar()
# textbox_inttime = ttk.Entry(root, textvariable=inttimetext, width='10')
# textbox_inttime.insert(0, '1000')
# button_inttime = ttk.Button(root, text='Set Integration time', state='disabled', width=30,
#                             command=setIntegrationTime)
# button_inttime.place(x=10, y=370)
#
# button_setLP = ttk.Button(root, text='Set Laser Power', state='disabled', width=30,
#                           command=setLaserPower)
# button_setLP.place(x=10, y=400)
# label_laserpower = ttk.Label(root, text='0-100%')
# LP = tk.StringVar()
# textbox_laserpower = ttk.Entry(root, textvariable=LP, width='10')
# textbox_laserpower.insert(0, '0')
#
#
# button_scan = ttk.Button(root, text='Scan', state='disabled', width=30,
#                          command=scan)
# button_scan.place(x=10, y=430)
#
# label_CDC = ttk.Label(root, text='')
# label_CDC.place(x=250, y=430)
# button_CDC = ttk.Button(root, text='Channel Difference Calibration', state='disabled', width=30,
#                         command=CDC)
# button_CDC.place(x=10, y=460)
#
# button_close = ttk.Button(root, text='Close device', state='disabled', width=30,
#                           command=close)
# button_close.place(x=10, y=490)

root.mainloop()
