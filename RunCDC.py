from ctypes import *
import pandas as pd
from scipy.signal import savgol_filter as sg_smoothing
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# import glob

modelname = 'BTC284N'

dll_path = 'bwtekusb.dll'
add_lib = CDLL(dll_path)

datapath = r'D:\Projects\Algorithm Study\USB\Data'
offsetpath = r'D:\Projects\Algorithm Study\USB\Data\offset'

# temperature unit is Celsius degree
Temperature_array = [-25]
# integration time unit is s
IntegrationTime_array = [1, 5, 10, 30]
Gain_array = np.arange(10000, 60000, 1000)
# Offset_array = np.arange(100, 4001, 100)
Offset_array = [2000]
# Offset_array = [2000]

# USBtype = c_int(0)
Channel = c_int(0)
PixelNum = 512
OutFileEEPROM = c_wchar_p('p')
TimingMode = c_int(1)
xarray = np.arange(0, PixelNum, 1)

InputMode = c_int(2)
Param = c_int(0)

data_array = (c_ushort * PixelNum)()
trigger = c_int(0)

Command = c_int(0x41)
ADValue = c_int(0)
DAChannel = 0
Set_Temperature = c_double(0)
Read_Temperature = c_double(0)
SetModeValue = c_int(0)

_type = []
_temperature = []
_integration = []
_gain = []
_offset = []
_std = []

# LE = 4
# CCode = (c_byte * LE)()
ccode = ''


# load parafile
# parafile = []


# get model from reading spectrometer type but not from model
def get_model():
    return 'model_name'


def get_ccode():
    return 'str of ccode'


def match_model():
    global Temperature_array
    global IntegrationTime_array
    model = get_model()
    if model == 'BTC284N':
        Temperature_array = [-25]
        IntegrationTime_array = [1000, 5000, 10000]
        return True
    elif model == 'BTC281Y':
        Temperature_array = [-20]
        IntegrationTime_array = [1000, 5000]
        return True
    else:
        return False


#
# def getpixelnum(parafile):
#     return 'pixelnum'
# return_on_ccode = add_lib.GetCCode(byref(CCode), Channel)
# cc = ''
# for i in range(LE):
#     cc += chr(CCode[i])
#     print(cc)

def calc_STD(ydata):
    y_SGSmooth = sg_smoothing(ydata, 99, 3)
    y_Straighten = ydata - y_SGSmooth
    STD_straighten = y_Straighten.std()
    return STD_straighten


def find_minimum(datafile):
    column_0 = datafile.iloc[:, 0]
    column_1 = datafile.iloc[:, 1]
    row_number = len(column_0)
    row_number_array = np.arange(0, row_number, 1)
    min_values = []
    for k in row_number_array:
        if column_1[k] == min(column_1):
            min_values.append(column_0[k])
            min_values.append(column_1[k])
            break
    return min_values


def find_optimized_offset(datafile):
    offset_column = datafile['Offset']
    std_column = datafile['STD']
    offset_interp_column = np.arange(100, 4001, 1)
    tck = interpolate.splrep(offset_column, std_column, s=0)
    std_interp_column = interpolate.splev(offset_interp_column, tck, der=0)
    df_1 = pd.DataFrame({'offset_column': offset_column,
                         'STD column': std_column})
    df_2 = pd.DataFrame({'Offset_interp': offset_interp_column,
                         'STD_interp': std_interp_column})
    min_values = find_minimum(df_1)
    min_values_interp = find_minimum(df_2)
    data_return = [min_values[0], min_values[1], min_values_interp[0], min_values_interp[1]]
    return data_return


def find_optimized_gain(datafile):
    gain_column = datafile['Gain']
    std_column = datafile['STD']
    gain_interp_column = np.arange(10000, 50001, 100)
    tck = interpolate.splrep(gain_column, std_column, s=0)
    std_interp_column = interpolate.splev(gain_interp_column, tck, der=0)
    df_1 = pd.DataFrame({'Gain_column': gain_column,
                         'STD column': std_column})
    df_2 = pd.DataFrame({'Gain_interp': gain_interp_column,
                         'STD_interp': std_interp_column})
    min_values = find_minimum(df_1)
    min_values_interp = find_minimum(df_2)
    data_return = [min_values[0], min_values[1], min_values_interp[0], min_values_interp[1]]
    return data_return


isInitialized = add_lib.InitDevices()
if not isInitialized:
    print('initialization fails. ')
else:
    # getEEPROM = add_lib.bwtekReadEEPROMUSB('p', Channel)
    # if getEEPROM:
    #     ccode = getccode(parafile)
    #     PixelNum = getpixelnum(parafile)
    # else:
    #     print('No EEPROM content is available')

    # auto check if model is qualified
    # isModelMatched = match_model()
    # assume model is qualified
    isModelMatched = True
    if isModelMatched:
        isCommunicated = add_lib.bwtekTestUSB(TimingMode, PixelNum, InputMode, Channel, Param)
        if isCommunicated < 0:
            print('Device communication error')
        else:
            add_lib.bwtekSetInGaAsMode(1, Channel)
            add_lib.bwtekGetInGaAsMode(byref(SetModeValue), Channel)
            if SetModeValue.value == 0:
                print('Detector mode is High Sensitivity')
            else:
                print('Detector mode is High Dynamic Range !\n')
            os.chdir(datapath)
            for temperature in Temperature_array:
                temp_set_count = 0
                add_lib.bwtekReadTemperature(Command, byref(ADValue), byref(Read_Temperature), Channel)
                print('Initial detector temperature is ', Read_Temperature.value)
                # detector temperature stabilization
                while abs(Read_Temperature.value - temperature) > 1.0 and temp_set_count <= 20:
                    add_lib.bwtekSetTemperatureUSB(DAChannel, temperature, Channel)
                    temp_set_count += 1
                    time.sleep(2)
                    add_lib.bwtekReadTemperature(Command, byref(ADValue), byref(Read_Temperature), Channel)
                else:
                    if temp_set_count > 20:
                        print('Detector cannot be stabilized. Current temperature is {}'.format(Read_Temperature.value))
                    else:
                        print('Stabilized temperature is {}...\n'.format(Read_Temperature.value))
                        # abandon the first data right after temperature change
                        add_lib.bwtekSetTimeUSB(200, Channel)
                        add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
                        #
                        for Integration in IntegrationTime_array:
                            add_lib.bwtekSetTimeUSB(Integration * 1000000, Channel)
                            # begin for offset calibration
                            # offset scans with laser off, set gain as 40000
                            gain_value = 40000
                            add_lib.bwtekSetAnalogOut(5, gain_value, Channel)
                            df = pd.DataFrame({'Pixel': xarray})
                            std_array = []
                            for offset_value in Offset_array:
                                add_lib.bwtekSetAnalogOut(4, int(offset_value), Channel)
                                isDataReadSuccessful = add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
                                if isDataReadSuccessful == PixelNum:
                                    DT = []
                                    for j in range(PixelNum):
                                        DT.append(data_array[j])
                                    df[str(offset_value)] = DT
                                    DT = np.array(DT)
                                    std_array.append(calc_STD(DT))
                                    print('offset {} is done !'.format(offset_value))
                                    plt.plot(xarray, DT)
                            # filename = str(temperature) + '_' + str(Integration) + '_' + 'offset.csv'
                            # df.to_csv(filename, index=False)
                            # plt.plot(Offset_array, std_array)
                            # df2 = pd.DataFrame({'Offset': Offset_array,
                            #                     'STD': std_array})
                            # optimized_offset = find_optimized_offset(df2)
                            # print('Optimized offset is {} where standard deviation is {} at temperature {} degree '
                            #       'and integration time {}s'.format(optimized_offset[2], optimized_offset[3],
                            #                                         temperature, Integration))
                            # _type.append('O')
                            # _temperature.append(temperature)
                            # _integration.append(Integration)
                            # _gain.append(40000)
                            # _offset.append(optimized_offset[2])
                            # _std.append(optimized_offset[3])

                            # end for offset calibration
                            # begin for gain calibration
                            # # gain scans with laser on, set optimized offset obtained above
                            # offset_value = optimized_offset[2]
                            # add_lib.bwtekSetAnalogOut(4, offset_value, Channel)
                            # df = pd.DataFrame({'Pixel': xarray})
                            # std_array = []
                            # for gain_value in Gain_array:
                            #     add_lib.bwtekSetAnalogOut(5, int(gain_value), Channel)
                            #     isDataReadSuccessful = add_lib.bwtekDataReadUSB(trigger, byref(data_array), Channel)
                            #     if isDataReadSuccessful == PixelNum:
                            #         DT = []
                            #         for j in range(PixelNum):
                            #             DT.append(data_array[j])
                            #         df[str(gain_value)] = DT
                            #         DT = np.array(DT)
                            #         std_array.append(calc_STD(DT))
                            #         print('Gain {} is done !'.format(gain_value))
                            # filename = str(temperature) + '_' + str(Integration) + '_' + 'gain.csv'
                            # df.to_csv(filename, index=False)
                            # plt.plot(Gain_array, std_array)
                            # df2 = pd.DataFrame({'Gain': Gain_array,
                            #                     'STD': std_array})
                            # optimized_gain = find_optimized_gain(df2)
                            # # print('Optimized gain is {} where standard deviation is {} at temperature {} degree '
                            # #       'and integration time {}s'.format(optimized_gain[2], optimized_gain[3],
                            # #                                          temperature, Integration))
                            # _type.append('G')
                            # _temperature.append(temperature)
                            # _integration.append(Integration)
                            # _gain.append(optimized_gain[2])
                            # _offset.append(optimized_offset[2])
                            # _std.append(optimized_gain[3])
                            # end for gain calibration
            df3 = pd.DataFrame({'Type': _type,
                                'Temperature': _temperature,
                                'Integration time(s)': _integration,
                                'Optimized Gain': _gain,
                                'Optimized offset': _offset,
                                'Standard deviation': _std})
            df3.to_csv('CDCalibration.csv', index=False)
    isUSBClosed = return_on_closeUSB = add_lib.bwtekCloseUSB(Channel)
    if isUSBClosed:
        print('USB device is disconnected.')
add_lib.CloseDevices()
plt.show()
