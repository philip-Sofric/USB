import time
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from ctypes import *
import pandas as pd
# from scipy import interpolate
import numpy as np
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import time
import os
from spectrotestfunctions import *

# OutFileEEPROM = c_wchar_p('p')

SpectrometerType = 17
Model = ''
PixelNum = 512
TimingMode = c_int(1)
InputMode = c_int(2)
Param = c_int(0)

# InGaAs mode
InGaAsMode = ('High Sensitivity', 'High Dynamic')
getModeValue = c_int(0)
setModelValue = c_int(0)

# Temperature
Command1 = c_int(0x41)
Command2 = c_int(0x42)
ADValue = c_int(0)
DAChannel1 = 0
DAChannel2 = 1

setTemperature1 = -20
setTemperature2 = 30
getTemperature1 = c_double(-10)
getTemperature2 = c_double(20)

# gain and offset
gain = 10000
offset = 1000

integration_time = 1000
laser_power = 0
trigger = c_int(0)
Channel = c_int(0)

detector_temperature_array = [-25]
chamber_temperature_array = [20]
integration_time_array = [1000]

gain_array = np.arange(10000, 60001, 1000)
offset_array = np.arange(100, 4001, 100)

modelwith2stagecooling = ['BTC284N', 'BTC281Y', 'HHEX']
modelwithCDC = ['BTC284N', 'BTC281Y', 'HHEX']

datapath = r'C:\Users\4510042\PycharmProjects\USB\Data'


def initialization():
    label_initialize = ttk.Label(root, text='')
    label_initialize.place(x=250, y=10)
    isInitialized = add_lib.InitDevices()
    global button_readEEPROM
    if isInitialized:
        label_initialize['text'] = 'device is initialized'
        button_readEEPROM['state'] = 'normal'
    else:
        label_initialize['text'] = 'device initialization fails'
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
    global detector_temperature_array
    global chamber_temperature_array
    global integration_time_array
    # global DAChannel1
    # global DAChannel2
    if spmodel == 'BTC284N':
        Command1 = 0x41
        Command2 = 0x42
        detector_temperature_array = [-25]
        chamber_temperature_array = [20]
        integration_time_array = [1000, 5000, 10000]
    elif spmodel == 'BTC281Y':
        Command1 = 0x61
        Command2 = 0x62
        detector_temperature_array = [-25]
        chamber_temperature_array = [20]
        integration_time_array = [1000, 5000, 10000]


def testUSB():
    label_testUSB.place(x=250, y=70)
    isCommunicated = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
    global button_GetInGaAsMode
    global button_SetInGaAsMode
    if isCommunicated < 0:
        label_testUSB['text'] = 'Communication error'
    else:
        label_testUSB['text'] = 'Device is ready'
        button_inttime['state'] = 'normal'
        label_inttime.place(x=220, y=340)
        textbox_inttime.place(x=350, y=340)
        button_scan['state'] = 'normal'
        button_CDC['state'] = 'normal'
        button_close['state'] = 'normal'
        if Model.startswith('BTC26') or Model.startswith('BTC28'):
            button_GetInGaAsMode['state'] = 'normal'
            button_SetInGaAsMode['state'] = 'normal'
            listbox_IGA.place(x=500, y=130)
        if Model in modelwith2stagecooling:
            button_readTemperature1['state'] = 'normal'
            button_readTemperature2['state'] = 'normal'
            button_setTemperature1['state'] = 'normal'
            button_setTemperature2['state'] = 'normal'
            label_setDetectorT.place(x=250, y=220)
            textbox_setDetectorTemp.place(x=400, y=220)
            label_setChamberT.place(x=250, y=250)
            textbox_setChamberTemp.place(x=400, y=250)
        if Model in modelwithCDC:
            # button_readGain_Offset['state'] = 'normal'
            button_setGain_Offset['state'] = 'normal'
            label_gain.place(x=250, y=310)
            textbox_gain.place(x=350, y=310)
            label_offset.place(x=450, y=310)
            textbox_offset.place(x=550, y=310)
            button_CDC['state'] = 'normal'


def getInGaAsMode():
    label_getIGA = ttk.Label(root, text='')
    label_getIGA.place(x=250, y=100)
    add_lib.bwtekGetInGaAsMode(byref(getModeValue), Channel)
    if getModeValue.value == 0:
        label_getIGA['text'] = 'InGaAs mode is high sensitivity'
    elif getModeValue.value == 1:
        label_getIGA['text'] = 'InGaAs mode is high dynamic range'
    else:
        label_getIGA['text'] = 'unable to get InGaAs working mode'


def setIGAValue(event):
    global setModelValue
    selected_index = listbox_IGA.curselection()[0]
    setModelValue = c_int(selected_index)
    # print(setModelValue)


def setInGaAsMode():
    label_setIGA = ttk.Label(root, text='')
    label_setIGA.place(x=250, y=130)
    add_lib.bwtekSetInGaAsMode(setModelValue, Channel)
    getInGaAsMode()
    if setModelValue.value == 0:
        label_setIGA['text'] = 'InGaAs mode is set high sensitivity'
    elif setModelValue.value == 1:
        label_setIGA['text'] = 'InGaAs mode is set high dynamic range'
    else:
        label_setIGA['text'] = 'Wrong'


def getTemperature_stage1():
    label_getTemp1 = ttk.Label(root, text='')
    label_getTemp1.place(x=250, y=160)
    isreadTemp1 = add_lib.bwtekReadTemperature(Command1, byref(ADValue), byref(getTemperature1), Channel)
    if isreadTemp1 > 0:
        label_getTemp1['text'] = f'Detector temperature is {getTemperature1.value:6.4}'
    else:
        label_getTemp1['text'] = 'Detector temperature read fails'


def getTemperature_stage2():
    label_getTemp2 = ttk.Label(root, text='')
    label_getTemp2.place(x=250, y=190)
    isreadTemp2 = add_lib.bwtekReadTemperature(Command2, byref(ADValue), byref(getTemperature2), Channel)
    if isreadTemp2 > 0:
        label_getTemp2['text'] = f'Chamber temperature is {getTemperature2.value:6.4}'
    else:
        label_getTemp2['text'] = 'Chamber temperature read fails'


def setTemperature_stage1():
    global setTemperature1
    setTemperature1 = int(setDetectorT.get())
    print(type(setTemperature1))
    issetDT = add_lib.bwtekSetTemperatureUSB(0, setTemperature1, Channel)
    if issetDT:
        print('yes')
    else:
        print('no')
    # time.sleep(5)
    getTemperature_stage1()


def setTemperature_stage2():
    global setTemperature2
    setTemperature2 = int(setChamberT.get())
    issetCT = add_lib.bwtekSetTemperatureUSB(DAChannel2, setTemperature2, Channel)
    if issetCT:
        print('yes')
    else:
        print('no')
    time.sleep(5)
    getTemperature_stage2()


def getGainOffset():
    pass


def setGainOffset():
    global gain
    global offset
    gain = int(gaintext.get())
    offset = int(offsettext.get())
    print(gain, offset)
    add_lib.bwtekSetAnalogOut(5, int(gain), Channel)
    add_lib.bwtekSetAnalogOut(4, int(offset), Channel)


def setIntegrationTime():
    global integration_time
    integration_time = int(inttimetext.get())
    add_lib.bwtekSetTimeUSB(integration_time * 1000, Channel)
    print(f'Integration time is set to {integration_time} ms')


def scan():
    xarray = np.arange(0, PixelNum, 1)
    data_array = (c_ushort * PixelNum)()
    figure = Figure(figsize=(8, 4), dpi=100)
    display = figure.add_subplot()
    display.set_title('Spectrum')
    display.set_xlabel('Pixel')
    display.set_ylabel('Intensity')
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().place(x=300, y=450)
    DT = []
    isDataReadSuccessful = add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
    if isDataReadSuccessful == PixelNum:
        for j in range(PixelNum):
            DT.append(data_array[j])
        DT = np.array(DT)
        display.plot(xarray, DT)
        canvas.draw()
    return xarray, DT


def CDC():
    label_CDC['text'] = 'Scanning'
    # set IGA mode to high sensitivity
    add_lib.bwtekSetInGaAsMode(0, Channel)
    os.chdir(datapath)
    _type = []
    _temperature = []
    _integration = []
    _gain = []
    _offset = []
    _std = []
    for temperature in detector_temperature_array:
        temp_set_count = 0
        add_lib.bwtekReadTemperature(Command1, byref(ADValue), byref(getTemperature1), Channel)
        label_CDC['text'] = f'Initial detector temperature is {getTemperature1.value:6.4}'
        # detector temperature stabilization
        while abs(getTemperature1.value - temperature) > 1.0 and temp_set_count <= 20:
            add_lib.bwtekSetTemperatureUSB(DAChannel1, temperature, Channel)
            temp_set_count += 1
            time.sleep(2)
            add_lib.bwtekReadTemperature(Command1, byref(ADValue), byref(getTemperature1), Channel)
        if temp_set_count > 20:
            label_CDC['text'] = f'Detector cannot be stabilized. Current temperature is {getTemperature1.value}'
        else:
            label_CDC['text'] = f'Stabilized temperature is {getTemperature1.value}...\n'
        # no matter temperature is stabilized or not, calibration continues...
        # abandon the first data right after temperature change
        add_lib.bwtekSetTimeUSB(200, Channel)
        label_CDC['text'] = 'Scanning'
        xarray, yarray = scan()
        label_CDC['text'] = 'First scan after temp change is abandoned'
        for Integration in integration_time_array:
            add_lib.bwtekSetTimeUSB(Integration * 1000, Channel)
            # begin for offset calibration. Offset scans with laser off, set gain as 40000
            std_array = []
            df = pd.DataFrame({'Pixel': xarray})
            gain_value = 40000
            add_lib.bwtekSetAnalogOut(5, gain_value, Channel)
            for offset_value in offset_array:
                add_lib.bwtekSetAnalogOut(4, int(offset_value), Channel)
                label_CDC[
                    'text'] = f'Scanning: temp {temperature}, time {Integration}, gain {gain_value}, offset {offset_value}'
                xarray, yarray = scan()
                std_array.append(calc_STD(yarray))
                df[str(offset_value)] = yarray
            filename = str(temperature) + '_' + str(Integration) + '_' + 'offset.csv'
            df.to_csv(filename, index=False)
            figure2 = Figure(figsize=(8, 4), dpi=100)
            display2 = figure2.add_subplot()
            display2.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
            display2.set_xlabel('Offset')
            display2.set_ylabel('Standard deviation')
            canvas = FigureCanvasTkAgg(figure2, master=root)
            canvas.get_tk_widget().place(x=300, y=450)
            display2.plot(offset_array, std_array)
            df2 = pd.DataFrame({'Offset': offset_array, 'STD': std_array})
            optimized_offset = find_optimized_offset(df2)
            label_CDC['text'] = f'Optimized offset is {optimized_offset[2]}'

            _type.append('O')
            _temperature.append(temperature)
            _integration.append(Integration)
            _gain.append(40000)
            _offset.append(optimized_offset[2])
            _std.append(optimized_offset[3])
            # end for offset calibration
            # # begin for gain calibration. gain scans with laser on, set optimized offset obtained above
            # std_array = []
            # df = pd.DataFrame({'Pixel': xarray})
            # offset_value = optimized_offset[2]
            # add_lib.bwtekSetAnalogOut(4, offset_value, Channel)
            # for gain_value in gain_array:
            #     add_lib.bwtekSetAnalogOut(5, int(gain_value), Channel)
            #     label_CDC[
            #         'text'] = f'Scanning: temp {temperature}, time {Integration}, gain {gain_value}, offset {offset_value} '
            #     xarray, yarray = scan()
            #     std_array.append(calc_STD(yarray))
            #     df[str(gain_value)] = yarray
            # filename = str(temperature) + '_' + str(Integration) + '_' + 'gain.csv'
            # df.to_csv(filename, index=False)
            # figure3 = Figure(figsize=(8, 4), dpi=100)
            # display3 = figure3.add_subplot()
            # display3.set_title(f'STD curve @ temperature {temperature} : integration time {Integration}')
            # display3.set_xlabel('Gain')
            # display3.set_ylabel('Standard deviation')
            # canvas = FigureCanvasTkAgg(figure3, master=root)
            # canvas.get_tk_widget().place(x=300, y=450)
            # display3.plot(gain_array, std_array)
            # df2 = pd.DataFrame({'Gain': gain_array, 'STD': std_array})
            # optimized_gain = find_optimized_offset(df2)
            # label_CDC['text'] = f'Optimized gain is {optimized_gain[2]} @ offset {offset_value}'
            #
            # _type.append('G')
            # _temperature.append(temperature)
            # _integration.append(Integration)
            # _gain.append(optimized_gain[2])
            # _offset.append(optimized_offset[2])
            # _std.append(optimized_gain[3])
            # # end for gain calibration
    df3 = pd.DataFrame({'Type': _type,
                        'Temperature': _temperature,
                        'Integration time(s)': _integration,
                        'Optimized Gain': _gain,
                        'Optimized offset': _offset,
                        'Standard deviation': _std})
    df3.to_csv('CDCalibration.csv', index=False)
    label_CDC['text'] = 'Done'


def close():
    isUSBClosed = return_on_closeUSB = add_lib.bwtekCloseUSB(Channel)
    if isUSBClosed:
        label_testUSB['text'] = 'Device is closed'
        button_inttime['state'] = 'disabled'
        button_scan['state'] = 'disabled'
        button_GetInGaAsMode['state'] = 'disabled'
        button_SetInGaAsMode['state'] = 'disabled'
        button_readTemperature1['state'] = 'disabled'
        button_readTemperature2['state'] = 'disabled'
        button_setTemperature1['state'] = 'disabled'
        button_setTemperature2['state'] = 'disabled'
        button_setGain_Offset['state'] = 'disabled'
        button_scan['state'] = 'disabled'
        button_CDC['state'] = 'disabled'


dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)

root = tk.Tk()
root.title('SpectroTest')
root.geometry('1200x900+50+50')
root.resizable(True, True)

button_initialize = ttk.Button(root, text='Initialize spectrometer', width=30, command=initialization)
button_initialize.place(x=10, y=10)

button_readEEPROM = ttk.Button(root, text='Read EEPROM', state='disabled', width=30, command=readEEPROM)
button_readEEPROM.place(x=10, y=40)

label_testUSB = ttk.Label(root, text='')
button_TestUSB = ttk.Button(root, text='Test USB', state='disabled', width=30, command=testUSB)
button_TestUSB.place(x=10, y=70)

button_GetInGaAsMode = ttk.Button(root, text='Get InGaAs mode', state='disabled', width=30, command=getInGaAsMode)
button_GetInGaAsMode.place(x=10, y=100)

button_SetInGaAsMode = ttk.Button(root, text='Set InGaAs mode', state='disabled', width=30, command=setInGaAsMode)
button_SetInGaAsMode.place(x=10, y=130)

InGaAs = tk.StringVar(value=InGaAsMode)
listbox_IGA = tk.Listbox(root, listvariable=InGaAs, height=2, selectmode='browse')
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

label_setDetectorT = ttk.Label(root, text='Detector T (-25 to 0)')
setDetectorT = tk.StringVar()
textbox_setDetectorTemp = ttk.Entry(root, textvariable=setDetectorT, width=10)
textbox_setDetectorTemp.insert(0, '-25')

button_setTemperature2 = ttk.Button(root, text='Set chamber temperature', state='disabled', width=30,
                                    command=setTemperature_stage2)
button_setTemperature2.place(x=10, y=250)

label_setChamberT = ttk.Label(root, text='Chamber T (10 to 30)')
setChamberT = tk.StringVar()
textbox_setChamberTemp = ttk.Entry(root, textvariable=setChamberT, width=10)
textbox_setChamberTemp.insert(0, '20')

label_gain = ttk.Label(root, text='Gain (0-65535)')
gaintext = tk.StringVar()
textbox_gain = ttk.Entry(root, textvariable=gaintext, width='10')
textbox_gain.insert(0, '10000')

label_offset = ttk.Label(root, text='Offset (0-4095)')
offsettext = tk.StringVar()
textbox_offset = ttk.Entry(root, textvariable=offsettext, width='10')
textbox_offset.insert(0, '100')

button_readGain_Offset = ttk.Button(root, text='Read Gain and Offset', state='disabled', width=30,
                                    command=getGainOffset)
button_readGain_Offset.place(x=10, y=280)

button_setGain_Offset = ttk.Button(root, text='Set Gain and Offset', state='disabled', width=30,
                                   command=setGainOffset)
button_setGain_Offset.place(x=10, y=310)

label_inttime = ttk.Label(root, text='Integration time (ms)')
inttimetext = tk.StringVar()
textbox_inttime = ttk.Entry(root, textvariable=inttimetext, width='10')
textbox_inttime.insert(0, '1000')
button_inttime = ttk.Button(root, text='Set Integration time', state='disabled', width=30,
                            command=setIntegrationTime)
button_inttime.place(x=10, y=340)

button_scan = ttk.Button(root, text='Scan', state='disabled', width=30,
                         command=scan)
button_scan.place(x=10, y=370)

label_CDC = ttk.Label(root, text='')
label_CDC.place(x=250, y=400)
button_CDC = ttk.Button(root, text='Channel Difference Calibration', state='disabled', width=30,
                        command=CDC)
button_CDC.place(x=10, y=400)

button_close = ttk.Button(root, text='Close device', state='disabled', width=30,
                          command=close)
button_close.place(x=10, y=430)

root.mainloop()
